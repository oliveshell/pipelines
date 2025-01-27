# Copyright 2021 The Kubeflow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from .utils import json_util
from . import lro_remote_runner


def deploy_model(
    type,
    project,
    location,
    payload,
    gcp_resources,
):
    """
  Deploy model and poll the LongRunningOperator till it reaches a final state.
  """
    api_endpoint = location + '-aiplatform.googleapis.com'
    vertex_uri_prefix = f"https://{api_endpoint}/v1/"
    # TODO(IronPan) temporarily remove the empty fields from the spec
    deploy_model_request = json_util.recursive_remove_empty(
        json.loads(payload, strict=False))
    endpoint_name = deploy_model_request['endpoint']
    deploy_model_url = f"{vertex_uri_prefix}{endpoint_name}:deployModel"

    remote_runner = lro_remote_runner.LroRemoteRunner(location)
    deploy_model_lro = remote_runner.create_lro(
        deploy_model_url, json.dumps(deploy_model_request), gcp_resources)
    deploy_model_lro = remote_runner.poll_lro(lro=deploy_model_lro)
