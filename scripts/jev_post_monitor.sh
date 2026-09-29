#!/bin/bash
# Change-detector for post 2101930064140968172 (deterministic output)
xurl "/2/tweets/2101930064140968172?tweet.fields=public_metrics" 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    m=d['data']['public_metrics']
    print(f\"imp={m['impression_count']} like={m['like_count']} reply={m['reply_count']} rt={m['retweet_count']} bm={m['bookmark_count']} quote={m['quote_count']}\")
except Exception as e:
    print('err', e)
"
