import replicate
import os
os.environ["REPLICATE_API_TOKEN"] = "r8_QMTKR3BK2GB8QNbaQzHAtRcoAMA7Lwg1PXPW1"
try:
    output = replicate.run(
        "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
        input={"prompt": "Write an essay on My Favorite Teacher in 200 words"}
    )
    # The meta/llama-2-70b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    print(output)
    for item in output:
        print(item, end="")
except Exception as e:
    print(e)