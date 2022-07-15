-- This is like a driver code to point to different ML servers and models
-- and seek ml_inbound_anomaly_score using such models
-- this ml driver is invoked by machine-learning-plugin-before.conf

-- currently most of this code is from https://github.com/coreruleset/coreruleset/pull/2067/files

-- set your machine learning server URL
local ml_server_url = 'http://localhost/ml-model-server/placeholder.py'

-- local variable for inbound_ml_status update. By default it must be zero 
local inbound_ml_status = 0

local ltn12 = require("ltn12")
local http = require("socket.http")

function main()

  local method = m.getvar("REQUEST_METHOD")
  local path = m.getvar("REQUEST_FILENAME")
  local hour = m.getvar("TIME_HOUR")
  local day = m.getvar("TIME_DAY")
  local args = m.getvars("ARGS")
  local args_str = "{}"
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
    url=url, 
    method='POST',
    source=source,
    headers=headers
  }

  if client == nil then
    m.log(4, 'The server is unreachable \n')
  end

  if code == 401 then
    m.log(4,'Anomaly found by ML')
  end

  if code == 200 then
    inbound_ml_status = 1
  end

  m.log(4, status, '\n')

  return inbound_ml_status

end
