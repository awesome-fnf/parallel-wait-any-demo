# -*- coding: utf-8 -*-
import json
import random
import time

from aliyunsdkcore import client
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkfnf.request.v20190315 import ReportTaskSucceededRequest
from aliyunsdkfnf.request.v20190315 import ReportTaskFailedRequest
from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException


def report_task_succeded(fnf_cli, task_token, output):
  request = ReportTaskSucceededRequest.ReportTaskSucceededRequest()
  request.set_Output(output)
  request.set_TaskToken(task_token)
  return fnf_cli.do_action_with_exception(request)


def report_task_failed(fnf_cli, task_token, error, cause):
  request = ReportTaskFailedRequest.ReportTaskFailedRequest()
  request.set_Error(error)
  request.set_TaskToken(task_token)
  request.set_Cause(cause)
  return fnf_cli.do_action_with_exception(request)


def handler(event, context):
  evt = json.loads(event)
  if 'task_token' not in evt:
    return '{"status": "child callback failed", "message": "no task_token in inputs."}'
  creds = context.credentials
  sts_token_credential = StsTokenCredential(creds.access_key_id, creds.access_key_secret, creds.security_token)
  fnf_cli = client.AcsClient(region_id=context.region, credential=sts_token_credential)

  """ this shows how to report task failed with error and cause.
  try:
    res = report_task_failed(fnf_cli, task_token=evt["task_token"], error=seed, cause="random error triggered")
  except ServerException as e:
    return '{"status": "child callback failed: %s"}' % e
  """  
  time.sleep(random.randint(1,5))
  try:
    res = report_task_succeded(fnf_cli, task_token=evt["task_token"],
                                 output='{"status":"from task %s input token: %s"}'
                                        % (evt["key"], evt["task_token"]))
  except ServerException as e:
    return '{"status": "child callback failed: %s"}' % e

  return '{"status": "child callback succeeded"}'