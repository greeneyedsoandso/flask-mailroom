import os

from flask import Flask, render_template, request, redirect, url_for
from peewee import IntegrityError, DoesNotExist

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all_donations'))


@app.route('/donations/')
def all_donations():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/select_donor/', methods=['GET', 'POST'])
def select_donor():
    if request.method == 'POST':
        name = request.form['donor']
        try:
            Donor.select().where(Donor.name == name).get()
            return donations_by_name(name)
        except DoesNotExist:
            return render_template('search_donor.jinja2', error=f'{name} is not'
                                                                f' in the database. Please'
                                                                f' check spelling and try again.')
    return render_template('search_donor.jinja2')


@app.route('/donation_history/<donor>/')
def donations_by_name(donor):
    donor_name = Donor.select().where(Donor.name == donor).get()
    donations = Donation.select().where(Donation.donor_id == donor_name.id)
    return render_template('single_donor.jinja2', donations=list(donations),
                           donor=donor.capitalize())


@app.route('/create/', methods=['GET', 'POST'])
def new_donation():
    if request.method == 'POST':
        try:
            donor = Donor(name=request.form['donor'].capitalize())
            donor.save()
            donation = Donation(value=request.form['value'], donor=donor.id)
            donation.save()
        except IntegrityError:
            donor = Donor.select().where(Donor.name == request.form['donor'].capitalize()).get()
            donation = Donation(value=request.form['value'], donor=donor.id)
            donation.save()
        return redirect(url_for('all_donations'))
    return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
    # app.run()
