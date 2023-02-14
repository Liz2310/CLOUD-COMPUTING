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

Examples of pagination: clicking through an archive of pictures, going through the results of a google search or turning the page of a book.

When using a GET API request to request information from a server, there could be thousands of entries in the returned JSON file. If the API result outputs thousands of entries at once, this is a drain of resources and a waste of time. It's better search through a server/database a little bit at a time. This when paging helps to query databases efficiently (helps to limit the number of results to help keep network traffic in check), and have API responses be more efficient.

There are many pagination methods:
- **Offset Pagination**
	- This methods allows clients to supply two additional parameters in their query: an _offset_, and a _limit_.
		- An offset is the number of records you wish to skip before selecting records.
		- A limit is the maximum number of entries to return.
	-	Example:
		-	If the request is to get the first page of the newest posts from a database, the API call might look like this:
			-	In this case the first page, containing the first 20 items, will be shown. (this will search 20 items at a time, and skip 0 of them).

				```GET /items?limit=20&offset=0```

			-	Now, if the second page is to be looked at, the next API call would look something like this:


				```GET /items?limit=20&offset=20```

				To fetch the next page of entries the API needs to be called with an *offset* parameter that equals the sum of the previous *offset* value and *limit* returned in the previous result, `new_offset = previous_offset + previous_limit`

	-	This method becomes slower as the number of records increases because the API still has to read up to the offset number of rows to know where it should start selecting data.
	-	Results can be faulty or missing because, if the API calls are made on databases that change frequently, the window of results will often be inaccurate across different pages in that you will either miss results entirely or see duplicates because results have now been added to the previous page.

- **Keyset Pagination**
	- Also known as the "seek method".
	- Instead of using the *offset* clause to skip rows to determine where the returned dataset should start, a *where* clause is used.
	- Example:
		- Considering a database with 1 000 000 rows, with an int _Id_ primary key column on which the data is sorted.
		To retrieve the first page:
		`GET /items?limit=50&after_id=0`
			```sql
			SELECT TOP 50 Id 
			FROM DataBaseExample
			WHERE Id > 0
			ORDER BY Id ASC
			```
			To retrieve the 10th page:
			`GET /items?limit=50&after_id=500`
			```sql
			SELECT TOP 50 Id 
			FROM DataBaseExample
			WHERE Id > 500
			ORDER BY Id ASC
			```

-	Using the *WHERE* clause and the index, the API does not need to go through _X_ number rows to find the correct starting point.
-	It features consistent ordering, even when new items are added to the database.
-	This can be done provided that the key used in the *WHERE* clause to implement the pagination is indexed and unique. 
	-	Both criteria are met by the concept of a primary key.
- Specific filtering can get complicated. Consider if the data is going to be sorted by a _CreatedDate_ column, and if two records have the same _CreatedDate_, then they should be sorted by _Id_.
	```sql
	SELECT TOP 50 DateCreated, Id 
	FROM OffSetDemo
	WHERE ((DateCreated > '2022/06/12') OR (DateCreated = '2022/06/12' AND Id > 500))
	ORDER BY DateCreated, Id ASC
	```
	- Depending on how many filter conditions there are, the *WHERE* clause could become complex.

## 3. Describe the concept of callback function. 15 points.


The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## 4. Describe the concept of cold start in AWS Lambda. 

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## 5. Describe each HTTP methods. 15 points.

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## 6. Describe how you can automate a deployment of a static website to S3. 15 points

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## 7. Read the Real-world [Engineering Challenges #8: Breaking up a Monolith](https://newsletter.pragmaticengineer.com/p/real-world-eng-8) article and write a summary and opinions about it. 10 points.
