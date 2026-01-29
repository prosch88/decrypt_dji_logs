# Decrypt DJI Logs
A simple python script to decode the android DJI app logs.

Based on this research: [Synacktiv](https://www.synacktiv.com/publications/dji-android-go-4-application-security-analysis), 
the AES-Keys for the logfiles are hardcoded. So the script decodes the Base64 text in the logs and then decrypts it with the Key / IV.

Usage:

```python
python decrypt_dji_logs <log_folder>
```

The output will be named as the input-folder with the suffix: _decrypted.

<br>
<br>
<br>


Like my work?
Maybe you'd like to buy me a coffee?

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I3I3H646F)
