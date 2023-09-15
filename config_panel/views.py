import traceback
import psycopg2
import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .credentials import *
from .log import *
import time

def visitor_ip_address(request):
    x_forwarded_for =request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return str(ip)

class bologinviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = bologinSerializer
    @swagger_auto_schema(request_body=bologinSerializer, operation_description="login")
    def post(self, request):
        req = request.data
        serializer = bologinSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "login"
        # graylog_io.info("REQ", req, method_name, str(client_ip))

        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        ipaddress = serializer.validated_data['ipaddress']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_login('{username}','{password}','{ipaddress}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class getservertimeviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    @swagger_auto_schema(operation_description="get_server_time")
    def get(self, request):
        req = request.data
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "getservertime"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur = conn.cursor()
            query = f"CALL Rpt_Getservertime();"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(query) +" | "+ str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:"+str(ts)+" | " + str(method_name)+ " | " + str(result) +" | "+ str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))
            # io_log.info("RES code:"+str(ts)+" | " + str(method_name)+ " | " + str(res) +" | "+ str(client_ip))
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class upd_kycdetailviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = kycupdatedetailSerializer
    @swagger_auto_schema(request_body=kycupdatedetailSerializer, operation_description="kyc_update")
    def post(self, request):
        req = request.data
        serializer = kycupdatedetailSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "update kycdetail"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        mobileno = serializer.validated_data['mobileno']
        Status = serializer.validated_data['Status']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_upd_kycdetail('{mobileno}',{Status});"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class kycdetailviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = kycdetailSerializer
    @swagger_auto_schema(request_body=kycdetailSerializer, operation_description="kyc_detail")
    def post(self, request):
        req = request.data
        serializer = kycdetailSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "kycdetail"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))
        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        mobileno = serializer.validated_data['mobileno']
        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur = conn.cursor()
            query = f"CALL rpt_kycdetail('{mobileno}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(query) +" | "+ str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:"+str(ts)+" | " + str(method_name)+ " | " + str(result) +" | "+ str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))
            # io_log.info("RES code:"+str(ts)+" | " + str(method_name)+ " | " + str(res) +" | "+ str(client_ip))
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class contestsCreationviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = contestsCreationSerializer
    @swagger_auto_schema(request_body=contestsCreationSerializer, operation_description="contest_creation")
    def post(self, request):
        req = request.data
        serializer = contestsCreationSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "contestcreation"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        contestname = serializer.validated_data['contestname']
        EntryFee = serializer.validated_data['EntryFee']
        Totalsports = serializer.validated_data['Totalsports']
        RankOne = serializer.validated_data['RankOne']
        WinPayout = serializer.validated_data['WinPayout']
        Maxwinngs = serializer.validated_data['Maxwinngs']
        Maxperuser = serializer.validated_data['Maxperuser']
        Scheme = serializer.validated_data['Scheme']
        Status = serializer.validated_data['Status']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_Ins_contestsCreation('{contestname}',{EntryFee},{Totalsports},'{RankOne}',{WinPayout},{Maxwinngs},{Maxperuser},'{Scheme}',{Status});"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class contestwisesalesviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = contestwiseSerializer

    @swagger_auto_schema(request_body=contestwiseSerializer, operation_description="contest_wise")
    def post(self, request):
        req = request.data
        serializer = contestwiseSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "contestwisesales"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_contestwisesales('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class managementreportviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = contestwiseSerializer

    @swagger_auto_schema(request_body=contestwiseSerializer, operation_description="management_report")
    def post(self, request):
        req = request.data
        serializer = contestwiseSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "managementreport"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_managementreport('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class playerwiseledgerviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = contestwiseSerializer

    @swagger_auto_schema(request_body=contestwiseSerializer, operation_description="player_wise_ledger")
    def post(self, request):
        req = request.data
        serializer = contestwiseSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "playerwiseledger"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_playerwiseledger('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            # print(result)
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class gamewisesalesdetailsviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = gamewisesalesdetailsSerializer

    @swagger_auto_schema(request_body=gamewisesalesdetailsSerializer, operation_description="game_wise_sales")
    def post(self, request):
        req = request.data
        serializer = gamewisesalesdetailsSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "gamewisesalesdetails"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        Status = serializer.validated_data['Status']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_gamewisesalesdetails('{fromdate}','{todate}',{Status});"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class addmoneydetailsviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = contestwiseSerializer

    @swagger_auto_schema(request_body=contestwiseSerializer, operation_description="addmoney_details")
    def post(self, request):
        req = request.data
        serializer = contestwiseSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "addmoneydetails"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_addmoneydetails('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class withdrawdetailsviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = contestwiseSerializer

    @swagger_auto_schema(request_body=contestwiseSerializer, operation_description="withdraw_details")
    def post(self, request):
        req = request.data
        serializer = contestwiseSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "withdrawdetails"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_withdrawdetails('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class playertransactionsummaryviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = contestwiseSerializer

    @swagger_auto_schema(request_body=contestwiseSerializer, operation_description="player_transaction_summary")
    def post(self, request):
        req = request.data
        serializer = contestwiseSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "playertransactionsummary"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_playertransactionsummary('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class playertransactiondetailsviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = playertransactiondetailsSerializer

    @swagger_auto_schema(request_body=playertransactiondetailsSerializer, operation_description="player_transaction_detail")
    def post(self, request):
        req = request.data
        serializer = playertransactiondetailsSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "playertransactiondetail"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        playerid = serializer.validated_data['playerid']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_playertransactiondetails('{fromdate}','{todate}','{playerid}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class changepasswordviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = changepasswordSerializer

    @swagger_auto_schema(request_body=changepasswordSerializer, operation_description="change_password")
    def post(self, request):
        req = request.data
        serializer = changepasswordSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "changepassword"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        username = serializer.validated_data['username']
        newpassword = serializer.validated_data['newpassword']
        ipaddress = serializer.validated_data['ipaddress']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_Changepassword('{username}','{newpassword}','{ipaddress}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserBlockactiveviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = UserBlockactiveSerializer

    @swagger_auto_schema(request_body=UserBlockactiveSerializer, operation_description="user_block_active")
    def post(self, request):
        req = request.data
        serializer = UserBlockactiveSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "userblock"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        username = serializer.validated_data['username']
        Status = serializer.validated_data['Status']
        ipaddress = serializer.validated_data['ipaddress']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_UserBlockactive('{username}',{Status},'{ipaddress}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class playerregistrationDetailviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = contestwiseSerializer

    @swagger_auto_schema(request_body=contestwiseSerializer, operation_description="playerregistrationDetail")
    def post(self, request):
        req = request.data
        serializer = contestwiseSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "playerregistrationDetail"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL rpt_playerregistrationDetail('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class dashboardviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = contestwiseSerializer

    @swagger_auto_schema(request_body=contestwiseSerializer, operation_description="dashboard")
    def post(self, request):
        req = request.data
        serializer = contestwiseSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "dashboard"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL RPT_DASHBOARD_TerminalDtls('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class dashboard_gamepayout_viewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = game_payoutSerializer

    @swagger_auto_schema(request_body=game_payoutSerializer, operation_description="dashboard game payout")
    def post(self, request):
        req = request.data
        serializer = game_payoutSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "dashboard game payout"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL RPT_Dashboard_Gamepayout('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class dashboard_overallpayout_viewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = game_payoutSerializer

    @swagger_auto_schema(request_body=game_payoutSerializer, operation_description="dashboard overall payout")
    def post(self, request):
        req = request.data
        serializer = game_payoutSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "dashboard overall payout"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        fromdate = serializer.validated_data['fromdate']
        todate = serializer.validated_data['todate']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL RPT_Dashboard_OverallPayout('{fromdate}','{todate}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class getdashboardswptviewset(GenericAPIView):
    permission_classes= (AllowAny,)
    @swagger_auto_schema(operation_description="get dashboard swpt")
    def get(self, request):
        req = request.data
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "get dashboard swpt"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur = conn.cursor()
            query = f"CALL RPT_DASHBOARD_SWPT();"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(query) +" | "+ str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:"+str(ts)+" | " + str(method_name)+ " | " + str(result) +" | "+ str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))
            # io_log.info("RES code:"+str(ts)+" | " + str(method_name)+ " | " + str(res) +" | "+ str(client_ip))
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class dashboard_monthwise_payout_viewset(GenericAPIView):
    permission_classes= (AllowAny,)
    serializer_class = monthwise_payoutSerializer

    @swagger_auto_schema(request_body=monthwise_payoutSerializer, operation_description="dashboard monthwise payout")
    def post(self, request):
        req = request.data
        serializer = monthwise_payoutSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "dashboard month wise payout"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        monthname = serializer.validated_data['monthname']
        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            conn.autocommit = True
            cur=conn.cursor()
            query = f"CALL RPT_DASHBOARD_MonthWise_payout('{monthname}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                    "success": True,
                    "result": result[0][0]
                }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class dashboard_monthwise_viewset(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = monthwise_payoutSerializer

    @swagger_auto_schema(request_body=monthwise_payoutSerializer, operation_description="dashboard monthwise")
    def post(self, request):
        req = request.data
        serializer = monthwise_payoutSerializer(data=req)
        client_ip = visitor_ip_address(request)
        req_id = str(time.time())
        method_name = "dashboard month wise"
        app_log.info("REQ", req_id, req, method_name, str(client_ip))

        # io_log.info("REQ code:"+str(ts)+" | " + str(method_name)+ " | " + str(req) +" | "+ str(client_ip))

        if not serializer.is_valid():
            res = {"Success": False, "errors": serializer.errors}
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + " | " + str(client_ip))
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        monthname = serializer.validated_data['monthname']

        try:
            conn = psycopg2.connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                                    port=DB_PORT)
            conn.autocommit = True
            cur = conn.cursor()
            query = f"CALL RPT_DASHBOARD_MonthWise('{monthname}');"
            app_log.info("DB-in", req_id, query, method_name, str(client_ip))
            # io_log.info("DB REQ code:" + str(ts) + " | " + str(method_name) + " | " + str(query) + " | " + str(client_ip))
            cur.execute(query)
            result = cur.fetchall()
            app_log.info("DB-out", req_id, str(result), method_name, str(client_ip))
            # io_log.info("DB RES code:" + str(ts) + " | " + str(method_name) + " | " + str(result) + "|" + str(client_ip))
            res = {
                "success": True,
                "result": result[0][0]
            }
            app_log.info("RES", req_id, res, method_name, str(client_ip))

            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # raise
            res = {'status': 1, 'Description': 500}
            tracbac = traceback.format_exc()
            err_log.exception(tracbac, req_id, str(e), method_name, request.data, client_ip)
            # io_log.info("RES code:" + str(ts) + " | " + str(method_name) + " | " + str(res) + "|" + str(client_ip))
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
