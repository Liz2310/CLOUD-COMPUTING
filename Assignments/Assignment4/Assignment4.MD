# Assignment 4

## 1. Describe the concept of throttling in APIs. 15 points.

Definition of throttle:
- to compress the throat of : _choke_
- to prevent or check expression or activity of : _suppress_

Now, taking these definitions to an API context, it means to limit the number or type of requests a user makes to an API (i.e. control the amount/type of traffic to an application) in a certain period of time. 

 >Throttling is a policy that the **Server** enforces and the **Client** respects.

The most common form ot API Throttling is Rate-Limit Throttling. For example, a click on a button from the user on a website, triggers a call to the site's API which interacts with the site's server, and does whatever action the button is intended to.

Now imagine where this happens on a site with a large number of users, the site is bound to show degradation in performance since it's receiving tons of request in short periods of time, this when Rate-Limit Throttling comes into play.

**How it is implemented:**
- There are many algorithms for this, but the steps can be resumed to the following:

	1.  Client calls an API that interfaces with a web application.
	2. The API throttling logic checks if the current request exceeds the allowed number of API calls.
	3. If the request is within limits, the API performs as usual and completes the user’s task.
	4. If the request exceeds the limit, the API returns an error response to the user.
	5. The user will have to wait for a pre-agreed time period, or pay to make any more API calls.

**Popular algorithms:** 
- **Leaky Bucket**
	- Uses a first-in, first-out (FIFO) queue (with a specific size) to hold the incoming requests.
	- If the queue still has space, it accepts requests by putting them at the end.
	- If the queue doesn't have space, it discards the request.

- **Fixed Window**
	- Allows N number of API calls from a user in a fixed time window.
	- At the start of the window, a counter is started at 0.
	- With every incoming request from a user, the counter is incremented.
	- If the counter reaches the limit (N) before the time window is over, new requests are declined.

- **Sliding Window**
	- Uses a time window like in Fixed Window.
	- The window time is broken down into smaller buckets.
	- Each bucket stores the request count corresponding to the bucket time range,  which constantly keeps moving across time.
	- Better visualized with an example for a sliding windows counter for a “5 requests/min” rate limiter, using each second as the window:
		- user_1 made a new request which creates an entry with the request time `9:01:01`as its hash key, with a counter set to `1`  for the `_:_:01` second window.
		- The user didn’t make any more requests until the `_:_:02` second window, where he makes `4` more requests.
			- Maxing out the “5 requests/min” limit for the `_:01:_` to `_:02:_` one-minute interval
		- All other requests for that interval would be dropped, till the start of a new window: `_:03:_`.

<p align="center">
  <img src="https://github.com/Liz2310/CLOUD-COMPUTING/blob/main/Assignments/Assignment4/images/sv.jpeg">
</p>

**Other Types of Throttling:**
- ***IP-Level Throttling***: You can make your API accessible only to a certain list of whitelisted IP addresses. 
	- You can also limit the number of requests sent by a certain client IP.
- ***Scope Limit Throttling***: Based on the classification of a user, you can restrict access to specific parts of the API - certain methods, functions, or procedures. 		
	-  Implementing scope limits can help you leverage the same API across different departments in the organization.
-   ***Concurrent Connections Limit***: Sometimes an application can't respond to more than a certain number of requests. In such cases, it's necessary limit the number of requests from a client (this ensures that other users don't face a DoS error). 
-   ***Resource-Level Throttling***: If a certain query returns a large result, the request can be throttled so that the SQL engine limits the number of rows returned.

**Benefits:**
- Users with better/faster connections might get a better experience than others. API throttling is a way ensure fair use of their APIs.
- Helps to fight back denial of service (DoS) attack, where malicious user(s) sends enormous volumes of requests to bring down a website or a mobile application.
- Helps to keep costs under control if an API consumes a large amount of resources or is linked to another ‘paid’ API.

## 2. Describe the concept of pagination in APIs. 15 points.

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## 3. Describe the concept of callback function. 15 points.


The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## 4. Describe the concept of cold start in AWS Lambda. 

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## 5. Describe each HTTP methods. 15 points.

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## 6. Describe how you can automate a deployment of a static website to S3. 15 points

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## 7. Read the Real-world [Engineering Challenges #8: Breaking up a Monolith](https://newsletter.pragmaticengineer.com/p/real-world-eng-8) article and write a summary and opinions about it. 10 points.
