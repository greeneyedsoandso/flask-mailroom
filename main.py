import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from peewee import IntegrityError

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all_donations'))


@app.route('/donations/')
def all_donations():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def new_donation():
    if request.method == 'POST':
        try:
            donor = Donor(name=request.form['donor'])
            donor.save()
            donation = Donation(value=request.form['value'], donor=donor.id)
            donation.save()
        except IntegrityError:
            donor = Donor.select().where(Donor.name == request.form['donor']).get()
            donation = Donation(value=request.form['value'], donor=donor.id)
            donation.save()
        return redirect(url_for('all_donations'))
    else:
        return render_template('create.jinja2')
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
    # app.run()
