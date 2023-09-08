from rest_framework import serializers

class bologinSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    ipaddress = serializers.CharField(max_length=255)

class kycupdatedetailSerializer(serializers.Serializer):
    mobileno = serializers.CharField(max_length=255)
    Status = serializers.IntegerField()

class kycdetailSerializer(serializers.Serializer):
    mobileno = serializers.CharField(max_length=255)

class contestsCreationSerializer(serializers.Serializer):
    contestname = serializers.CharField(max_length=255)
    EntryFee = serializers.IntegerField()
    Totalsports = serializers.IntegerField()
    RankOne = serializers.CharField(max_length=255)
    WinPayout = serializers.IntegerField()
    Maxwinngs = serializers.IntegerField()
    Maxperuser = serializers.IntegerField()
    Scheme = serializers.CharField(max_length=255)
    Status = serializers.IntegerField()

class contestwiseSerializer(serializers.Serializer):
    fromdate = serializers.CharField(max_length=255)
    todate = serializers.CharField(max_length=255)


class gamewisesalesdetailsSerializer(serializers.Serializer):
    fromdate = serializers.CharField(max_length=255)
    todate = serializers.CharField(max_length=255)
    Status = serializers.IntegerField()

class playertransactiondetailsSerializer(serializers.Serializer):
    fromdate = serializers.CharField(max_length=255)
    todate = serializers.CharField(max_length=255)
    playerid = serializers.CharField(max_length=255)


class changepasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    newpassword = serializers.CharField(max_length=255)
    ipaddress = serializers.CharField(max_length=255)


class UserBlockactiveSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    Status = serializers.IntegerField()
    ipaddress = serializers.CharField(max_length=255)

class game_payoutSerializer(serializers.Serializer):
    fromdate = serializers.CharField(max_length=255)
    todate = serializers.CharField(max_length=255)


class monthwise_payoutSerializer(serializers.Serializer):
    monthname = serializers.CharField(max_length=30)

