from flask import Blueprint, render_template, request, redirect, abort
from utils import is_admin, admin_view_log, admin_list_log

admin = Blueprint('admin', __name__)


@admin.route("/admin")
def admin_home():
    if not is_admin(request):
        abort(403)
    return render_template("admin.html")


@admin.route("/admin/log/view", methods=["POST"])
def view_log():
    if not is_admin(request):
        abort(403)
    logfile = request.form.get("logfile")
    if logfile:
        logcontent = admin_view_log(logfile)
        return logcontent
    return ''


@admin.route("/admin/log/dir", methods=["POST"])
def list_log():
    if not is_admin(request):
        abort(403)
    logdir = request.form.get("logdir")
    if logdir:
        logdir = admin_list_log(logdir)
        return str(logdir)
    return ''
