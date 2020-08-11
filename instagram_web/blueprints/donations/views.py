from flask import Blueprint, redirect, render_template , request , url_for
from flask_login import login_required , current_user
import braintree
from instagram_web.util.helpers import gateway
from models.donation import Donation
from models.images import Images
from models.user import User
import requests
import os



donations_blueprint=Blueprint("donations",
                               __name__,
                               template_folder="templates")





@donations_blueprint.route("/new")
def new(image_id):
    client_token=gateway.client_token.generate()
    return render_template("donations/new.html" ,client_token=client_token , image_id=image_id)

@donations_blueprint.route('/' , methods=["POST"])
def create(image_id):
    amount=request.form.get("amount")
    print(amount)
    nonce_from_the_client=request.form.get("payment_method_nonce")
    print(nonce_from_the_client)
   

    result = gateway.transaction.sale({
        'amount':int(amount),
        'payment_method_nonce': nonce_from_the_client,
#   "device_data": device_data_from_the_client,
        'options': {
            'submit_for_settlement': True
        }
    })

    if result.is_success:
        # the reason why we have to get the instance for sender and can't use current_user straight away is because current_user itself is not an instance of User class.. its just object/instance from flask_login 
        donation=Donation(amount=amount, image=image_id , sender=User.get_by_id(current_user.id) )
        print(donation.sender)

        donation.save()
        mailgun_result=requests.post(
		f"https://api.mailgun.net/v3/{os.environ.get('MAILGUN_DOMAIN')}/messages",
		auth=("api", f"{os.environ.get('MAILGUN_API_KEY')}"),
		data={"from": "Mailgun Sandbox <postmaster@sandboxeaa30d1922044857bee3122cfe3ac0f9.mailgun.org>",
			"to": "WEI KHANG TAN <weikhang_93@hotmail.com>",
			"subject": "Hello WEI KHANG TAN",
			"text": "Congratulations WEI KHANG TAN, you just sent an email with Mailgun!  You are truly awesome!"})





    

    

    print(result)

    return "hehehe" 

@donations_blueprint.route('/')
def index(image_id):
    image=Images.get_or_none(Images.id==image_id)


    return render_template("/donations/index.html" , image=image)
