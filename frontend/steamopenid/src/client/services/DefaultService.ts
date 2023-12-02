/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OpenIDResponse } from '../models/OpenIDResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Callback
     * @returns any Successful Response
     * @throws ApiError
     */
    public static callbackAuthSteamCallbackPost({
requestBody,
}: {
requestBody: OpenIDResponse,
}): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/steam/callback',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Profile
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getProfileMeGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/me',
        });
    }

}
