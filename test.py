from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
import jwt

