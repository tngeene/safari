from flask import render_template, session, json, current_app, redirect, url_for, Blueprint, flash, g
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask import url_for, current_app, redirect, request
from rauth import OAuth2Service
from ..models import User
from .. import db
import json
import urllib, urllib3

http = urllib3.PoolManager()

social = Blueprint('social', __name__)



