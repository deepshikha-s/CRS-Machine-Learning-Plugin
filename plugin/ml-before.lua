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
--Added for using lfs.chdir() 
local lfs = require("lfs")
local respbody = {}

local function parse_urlencoded_type()

end

local function parse_multipart_type()

end

local function parse_json_type()

end

local function parse_xml_type()

end

function main()

--Added for fileIO
  local buf_all = {}
  local cwd = lfs.currentdir()
  m.log(4, "CWD is " ..cwd)
  local wdir = lfs.chdir("/tmp")
  cwd = lfs.currentdir()
  m.log(4, "New CWD is " ..cwd)
  tempfile = io.tempfile 
  filewrite = io.open("tempfile", "w")
  if filewrite then 
     filewrite:write("Test file: line 1")
     --filewrite:write(" Test file: line 2")
     --filewrite:write(" Test file: line 3")
     filewrite:close()
  else
     m.log(1, "FILE WRITE FAILED")
  end

  fileread = io.open("tempfile", "r")
  if fileread then 
     --cur = fileread:seek()
     buf_all=fileread:read("*all")
    m.log(1, "FILE content buf_all is:\n  " ..buf_all) 
    --size = fileread:seek("end")  
    --m.log(1, "File size "..size)  
    --fileread:seek("set", cur)
    size = fileread:seek("end")
    m.log(4, "File size "..size)  
--fileread:close()
  else
     m.log(1, "FILE READ FAILED")
  end

  local method = m.getvar("REQUEST_METHOD")
  local path = m.getvar("REQUEST_FILENAME")
  local hour = m.getvar("TIME_HOUR")
  local day = m.getvar("TIME_DAY")
  local reqbody = m.getvar("REQUEST_CONTENT_TYPE")
  local reqbodyl = m.getvar("REQUEST_BODY_LENGTH")
  local args = m.getvars("ARGS")
  local args_str = "{}"
  local req_data = {}
  req_data["req_protocol"] = m.getvar("REQUEST_PROTOCOL")
  req_data["req_uri"] = m.getvar("REQUEST_URI")
  req_data["req_method"] = m.getvar("REQUEST_METHOD")
  req_data["req_unique_id"] = m.getvar("UNIQUE_ID")
  req_data["file_name"] = m.getvar("REQUEST_FILENAME")
  req_data["base_name"] = m.getvar("REQUEST_BASENAME")
  req_data["headers_name"] = m.getvar("REQUEST_HEADERS_NAMES")
  m.log(1, "Inside before lua script")
  m.log(1, "RequestProtocol: " ..req_data["req_protocol"])
  m.log(1, "RequestURI: " ..req_data["req_uri"])
  m.log(1, "RequestMethod: " ..req_data["req_method"])
  m.log(1, "RequestUniqueID: " ..req_data["req_unique_id"])
  m.log(1, "RequestFilename: " ..req_data["file_name"])
  m.log(1, "RequestBasename: " ..req_data["base_name"])
  m.log(1, "RequestHeadersName: " ..req_data["headers_name"])
  m.log(1, "body " ..reqbody)
  m.log(1, "length "..reqbodyl)
  local rea_header = {}
  -- req_header["req_header_content_type"] = m.getvar("CONTENT_TYPE")
  -- req_header["req_header_content_type"] = m.getvar("REQUEST_HEADERS:Content-Type")
  -- req_header["req_header_content_length"] = m.getvar("REQUEST_HEADERS:Content-Length")

  -- m.log(1, "RequestHeaderContentType: " ..req_header["req_header_content_type"])
  -- m.log(1, "RequestHeaderContentLength: " ..req_header["req_header_content_length"])

  -- local content_length = m.getvar("CONTENT_LENGTH")
  -- local req_length = tonumber(m.getvar("CONTENT_LENGTH"))

  -- Start: this will not be in phase 1. Move this to -after.conf script or create new rule for phase2
    -- local req_body = {}
    -- req_body["req_body"] = m.getvar("REQUEST_BODY")
    -- req_body["req_body_length"] = m.getvar("REQUEST_BODY_LENGTH")
    -- m.log(1, "RequestBody: " ..req_body["req_body"])
    -- m.log(1, "RequestBodyLength: " ..req_body["req_body_length"])
  -- local req_body = m.getvar("REQUEST_BODY","urlDecodeUni")
  -- End: this will not be in phase 1. Move this to after script

  --if req_length > 0 then
  --    if string.find(req_type, "application/x-www-form-urlencoded", 1, true) then
  --    parse_urlencoded_type()
  --    elseif string.find(req_type, "multipart/form-data", 1, true) then
  --    parse_multipart_type()
  --    elseif string.find(req_type, "application/json", 1, true) then
  --    parse_json_type()
  --    elseif string.find(req_type, "application/xml", 1, true) then
  --    parse_xml_type()local req_data = {}
  --    end
  --end

  -- m.log(1,"Starting script execution \n")
  -- local fileHandle = assert(io.open('/tmp/req_body.txt','a'))
  -- fileHandle:write("--- Output start ---\n")
  -- fileHandle:write(m.getvar("REQUEST_BODY","urlDecodeUni"))
  -- fileHandle:write("\n --- Output end --- \n")
  -- m.log(1,"Script execution finished\n")

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
  --local headers = {
    --["Content-Type"] = "multipart/form-data";
    --["Content-Length"] = #body                   --modify
  --}
  local headers = {
    ["Content-Type"] = "multipart/form-data",
    ["Content-Length"] = 17                   
  }
  local source = ltn12.source.file(fileread)
  if not source then
    m.log(1, "source error")
  else
    m.log(1, "Sending http request from lua")
    local client, code, headers, status = http.request{
      url=ml_server_url, 
      method='POST',
      source=source,
      headers=headers,
      sink = ltn12.sink.table(respbody)
    }
    respbody = table.concat(respbody)
  end
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
