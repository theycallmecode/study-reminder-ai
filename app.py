# main application file

from flask import Flask, render_template, request, jsonify, redirect, url_for
from chat_model import StudyBotAI
from reminder_manager import ReminderManager
import os
from dotenv import load_dotenv