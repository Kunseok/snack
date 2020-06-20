CID="Q5qZGovtZuMVVqJyUq1Mwre7OtCOPE7despaC3GZ"
CS="iKSjolJcrIjefTk0Of2pMBZEQ5ZJBFh00teRSbwtBLysqRs9KsaEDaLZWOXo8a1pwz49umMu2b9rbZfoq7J6X13vjXIbTGVEcweuS0kECIESX4D7RY16RsvMEHGKV3iU"

CCID="1QT7Jc33NvO2U9pfDgIJBl4n3KfxUFpcxCLec37S"
CCS="v4FnV3oRK3AF2wqMLEDee1QdDAi2s5Rf1eUWtzIOTkmCGMBzk7rIijGO8e8hjWPlL272hda4aKWXGgS9TdNpCD0jFBktUHRVcTXBJASVcAvBkxlAwy9KgL3BO42mg4jM"

#curl -X POST 'http://authorization.oouch.htb:8000/oauth/token/' -H "Content-Type: application/x-www-form-urlencoded" --data "grant_type=client_credentials&client_id='$CID'&client_secret='$CS'" -L -s
curl ''' -X POST 'http://authorization.oouch.htb:8000/oauth/token/' -H "Content-Type: application/x-www-form-urlencoded" --data "grant_type=client_credentials&client_id='$CCID'&client_secret='$CCS'" -L -s'''
