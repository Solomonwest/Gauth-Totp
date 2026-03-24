GOOGLE AUTH-TOTP(TIME BASED OTP) Login System

NB: You can use any Time Based Application to setup, but I'll suggest ' Google Authenticator App '
As this is what was used for this program.

This is an enhanced 2FA System that makes use of Time based OTP to validate and verify on every login

Upon signing up, the user gets to create a TOTP device of which a QR Code and Secret Key is generated.
The user then gets to validate by inputing the recent token, if valid the user gets logged in.
Else A brand new TOTP device gets created and the user has to redo validation.

As for Signing in, The user just gets to input the recent token. If valid the user is then logged in.

Honest Comment -: " This is best and cheap for applications that requires Enhanced Security and wants to avoid using paid OTP services.
