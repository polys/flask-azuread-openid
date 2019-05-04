import json

import requests
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from flask import Flask, g, jsonify, Response
from flask_httpauth import HTTPTokenAuth
from jwcrypto import jwk, jws, jwt

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

cache_opts = {"cache.type": "memory"}
cache = CacheManager(**parse_cache_config_options(cache_opts))


@cache.cache("token_signing_keys", expire=300)
def _get_token_signing_keys():
    oid_config_url = "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
    oid_config = requests.get(oid_config_url).json()
    jwks_uri = oid_config.get("jwks_uri")
    jwks = requests.get(jwks_uri).content
    keys = jwk.JWKSet.from_json(jwks)
    return keys


@auth.error_handler
def _auth_error_handler():
    return ""


@auth.verify_token
def _auth_verify_token(id_token):
    g.user_claims = None

    if not id_token:
        return False

    try:
        keys = _get_token_signing_keys()
        token = jwt.JWT(key=keys, jwt=id_token)
        g.user_claims = json.loads(token.claims)
    except:
        return False

    return g.user_claims is not None


@app.route("/me", methods=["GET"])
@auth.login_required
def index():
    return jsonify(g.user_claims)


@app.errorhandler(404)
def not_found(error=None):
    return Response(status=404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
