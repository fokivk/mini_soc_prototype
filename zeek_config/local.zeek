# Zeek local configuration for attack detection

@load base/protocols/http
@load base/protocols/conn
@load base/frameworks/notice

# Define notice types for attacks
redef enum Notice::Type += {
    XSS_Attack,
    SQL_Injection_Attack
};

# XSS detection
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
{
    local uri = unescaped_URI;
    
    # Check for XSS patterns
    if (/<script/i in uri || /javascript:/i in uri || /onload=/i in uri || /onclick=/i in uri) {
        NOTICE([$note=XSS_Attack,
                $msg=fmt("XSS Attack detected in HTTP request: %s", uri),
                $conn=c,
                $identifier=cat(c$id$orig_h, c$id$resp_h, uri)]);
    }
    
    # Check for SQL injection patterns
    if (/UNION SELECT/i in uri || /OR 1=1/i in uri || /DROP TABLE/i in uri || 
        /INSERT INTO/i in uri || /DELETE FROM/i in uri || /UPDATE SET/i in uri) {
        NOTICE([$note=SQL_Injection_Attack,
                $msg=fmt("SQL Injection Attack detected in HTTP request: %s", uri),
                $conn=c,
                $identifier=cat(c$id$orig_h, c$id$resp_h, uri)]);
    }
}

# Create a custom log file for HTTP requests
type HTTP_Log: record {
    ts: time;
    method: string;
    uri: string;
    src_ip: addr;
    dst_ip: addr;
    user_agent: string &optional;
};

global http_log: file = open("/usr/local/zeek/logs/http_requests.log");

# Log all HTTP requests for analysis
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
{
    local log_entry: HTTP_Log = [
        $ts = network_time(),
        $method = method,
        $uri = unescaped_URI,
        $src_ip = c$id$orig_h,
        $dst_ip = c$id$resp_h
    ];
    
    if (c$http?$user_agent) {
        log_entry$user_agent = c$http$user_agent;
    }
    
    print http_log, log_entry;
    print fmt("HTTP Request: %s %s from %s to %s", method, unescaped_URI, c$id$orig_h, c$id$resp_h);
}

# Log connection statistics
event connection_state_remove(c: connection)
{
    if (c$resp$size > 0) {
        print fmt("Connection: %s:%d -> %s:%d, Bytes: %d", 
                 c$id$orig_h, c$id$orig_p, c$id$resp_h, c$id$resp_p, c$resp$size);
    }
}
