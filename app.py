import sys

import click
import flask
import flask_mail


app = flask.Flask(__name__)
app.config.from_object("config")

mail = flask_mail.Mail(app)


import model
import secretsanta


@app.route("/")
def home():
    return flask.redirect("https://de.wikipedia.org/wiki/Wichteln")


@app.route("/<secret_id>")
def draw(secret_id):
    secret = model.Secret.query.get(secret_id)

    if secret is None:
        return flask.abort(404)

    return flask.render_template("draw.html", secret=secret)


@app.cli.command()
@click.argument("config_file", type=click.File("rb"), default=sys.stdin)
def draw(config_file):
    config = secretsanta.read_config(config_file)
    partners = secretsanta.draw_partners(config)

    secrets = [
        (
            giver,
            config.get_person(giver),
            create_secret(
                config.get_person(giver),
                config.get_person(receiver),
                config.site_settings
            )
        )
        for giver, receiver in partners.items()
    ]

    print("\nIDs:")
    print("\n".join(
        "%s: %s" % (giver, secret.id)
        for giver, giver_info, secret in secrets
    ))

    messages = [
        create_mail(giver_info, secret, config.email_settings)
        for giver, giver_info, secret in secrets
    ]

    print("\nEmails:\n")
    print("\n\n".join(map(str, messages)))

    print("\nEmail addresses:")
    print("\n".join(", ".join(msg.recipients) for msg in messages))

    confirm = input("\ncontinue? [N/y]: ")
    if confirm != "y":
        print("Aborted.")
        return

    model.db.session.commit()

    for msg in messages:
        mail.send(msg)

    print("\nDone.")


def create_secret(giver, receiver, config):
    secret = model.Secret.create()

    secret.secret1 = render_string(config.get('secret1'), receiver)
    secret.secret2 = render_string(config['secret2'], receiver)
    secret.text_above = render_string(config.get('text_above'), giver)
    secret.text_below = render_string(config.get('text_below'), giver)
    secret.title = render_string(config.get('title'), giver)
    secret.signature = render_string(config.get('signature'), giver)

    model.db.session.add(secret)

    return secret


def create_mail(giver, secret, config):
    url = flask.url_for("draw", secret_id=secret.id, _external=True)

    msg = flask_mail.Message()
    msg.subject = render_string(config.get('subject'), giver)
    msg.body = render_string(config.get('message'), giver, url=url)
    msg.recipients = [render_string(config.get('receiver'), giver)]

    sender_name = render_string(config.get('sender'), giver)
    sender_email = app.config.get('MAIL_SENDER_EMAIL')

    if sender_name and sender_email:
        msg.sender = "%s <%s>" % (sender_name, sender_email)
    elif sender_name:
        msg.sender = sender_name
    elif sender_email:
        msg.sender = sender_email

    return msg


def render_string(template, person, **kwargs):
    if template is None:
        return ""
    else:
        kwargs.update(person)
        jinja_template = app.jinja_env.from_string(template)
        return jinja_template.render(**kwargs)


@app.cli.command()
@click.argument("recipient")
def testmail(recipient):
    msg = flask_mail.Message("Test", body="Test", recipients=[recipient])
    mail.send(msg)
