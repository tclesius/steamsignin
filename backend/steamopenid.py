from tkinter import N
from fastapi.datastructures import QueryParams
from fastapi.responses import RedirectResponse
import logging, os
from urllib.parse import urlencode
from urllib.request import urlopen
import re
from pydantic import BaseModel, AnyHttpUrl, Field

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('SSI_LOGLEVEL', 'WARNING').upper())
provider = 'https://steamcommunity.com/openid/login'


class OpenIDResponse(BaseModel):
    openid_ns: str = Field(alias='openid.ns')
    openid_mode: str = Field(alias='openid.mode')
    openid_op_endpoint: str = Field(alias='openid.op_endpoint')
    openid_claimed_id: str = Field(alias='openid.claimed_id')
    openid_identity: str = Field(alias='openid.identity')
    openid_return_to: str = Field(alias='openid.return_to')
    openid_response_nonce: str = Field(alias='openid.response_nonce')
    openid_assoc_handle: str = Field(alias='openid.assoc_handle')
    openid_signed: str = Field(alias='openid.signed')
    openid_sig: str = Field(alias='openid.sig')

class SteamOpenID:    
    @staticmethod
    def validate(openid_response: OpenIDResponse):
        logger.info('...')
        response = openid_response.model_dump(by_alias=True)
        params = {
            'openid.assoc_handle': response['openid.assoc_handle'],
            'openid.signed': response['openid.signed'],
            'openid.sig': response['openid.sig'],
            'openid.ns': response['openid.ns']
        }
        signed_args = response['openid.signed'].split(',')
        
        for item in signed_args:
            item_arg = f'openid.{item}'
            if response[item_arg] not in params:
                params[item_arg] = response[item_arg]

        params['openid.mode'] = 'check_authentication'

        logger.info('...')

        validation_response = requests.get(provider, params=params).text
        
        logger.info('...')

        if re.search('is_valid:true', validation_response):
            if(match := re.search('https://steamcommunity.com/openid/id/(\\d+)', response['openid.claimed_id'])):
                if (steamid := match.group(1)):
                    return steamid
            else:
                # If we somehow fail to get a valid steam64ID, just return None
                return None
        else:
            # Same again here
            return None
