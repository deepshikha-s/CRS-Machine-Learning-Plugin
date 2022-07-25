--import urllib.request
--import urllib.parse
-- This is like a driver code to point to different ML servers and models
-- and seek ml_inbound_status using such models
-- this ml driver is invoked by machine-learning-plugin-after.conf if
-- the anomaly score exceeds the threshold

-- currently most of this code is from https://github.com/coreruleset/coreruleset/pull/2067/files

-- set your machine learning server URL
local ml_server_url = 'http://127.0.0.1:5000/'
-- local variable for inbound_ml_status update. By default it must be zero 
local inbound_ml_result = 0
local ltn12 = require("ltn12")
local http = require("socket.http")
local respbody = {}

function main()
  local method = m.getvar("REQUEST_METHOD")
  local path = m.getvar("REQUEST_FILENAME")
  local hour = m.getvar("TIME_HOUR")
  local day = m.getvar("TIME_DAY")
  local args = m.getvars("ARGS")
  local args_str = "{}"
  local reqbody = m.getvar("CONTENT-TYPE")
  
  m.log(1, "Args ", reqbody)

  -- transform the args array into a string following JSON format
  if args ~= nil then
    args_str = "{"
    for k,v in pairs(args) do
      name = v["name"]
      value = v["value"]
      value = value:gsub('"', "$#$")
      args_str = args_str..'"'..name..'":"'..value..'",'
    end
    if #args == 0 then
      args_str = "{}"
    else
      args_str = string.sub(args_str, 1, -2)
      args_str = args_str.."}"
    end
  end

 -- construct http request for the ml server
  local body = "method="..method.."&path="..path.."&args="..args_str.."&hour="..hour.."&day="..day
  local headers = {
    ["Content-Type"] = "application/x-www-form-urlencoded";
    ["Content-Length"] = #body
  }
  local source = ltn12.source.string(body)
  local client, code, headers, status = http.request{
    url=ml_server_url, 
    method='POST',
    source=source,
    headers=headers,
    sink = ltn12.sink.table(respbody)
  }
  respbody = table.concat(respbody)
  if client == nil then
    m.log(1, 'The server is unreachable \n')
  end

  if code == 401 then
    inbound_ml_result = 0
    m.log(1,'Anomaly found by ML')
  end

  if code == 200 then
    inbound_ml_result = 1
  end
  m.setvar("TX.inbound_ml_anomaly_score", respbody)
  m.setvar("TX.inbound_ml_status", inbound_ml_result)
  return inbound_ml_result

end
