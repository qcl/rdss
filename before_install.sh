#!/bin/bash

if [ "${TRAVIS_PULL_REQUEST}" = "false" ]; then
    openssl aes-256-cbc -K $encrypted_938639410c7c_key -iv $encrypted_938639410c7c_iv -in rdss-api-gae.json.enc -out rdss-api-gae.json -d
fi
