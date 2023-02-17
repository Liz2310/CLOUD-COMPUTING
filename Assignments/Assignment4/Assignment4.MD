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
A callback function is a function that is passed as an argument to another function, to be “called back” at a later time.

A callback function always has a specific action which is bound to a specific circumstance. Therefore, a callback function is only called once a clearly defined operation has been performed.

The invocation may be immediate as in a synchronous callback or it might happen at later time, as in an asynchronous callback. 

- They are useful for asynchronous behavior where we want an activity to take place whenever a previous event completes (i.e. actions that are initiated now, but they finish later). 

A use case is when data is requested from other sources, such as an external API, it's not always know when the data will be served back. In these instances it's needed to wait for the response, but we it's not ideal to have the entire application grinding to a halt while the data is being fetched, this when callbacks become useful.

Example:

```javascript
function serverRequest(query, callback){
  setTimeout(function(){
    var response = query + "full!";
    callback(response);
  },5000);
}

function getResults(results){
  console.log("Response from the server: " + results);
}

serverRequest("The glass is half ", getResults);

// Result in console after 5 second delay:
// Response from the server: The glass is half full!
```

- The *serverRequest* takes a callback function as an argument.
	- It uses *setTimeout* to simulate an asynchronous operation.
		- It takes two arguments: a callback function and a delay time in milliseconds.
- After 5 seconds elapse the response is modified and then the callback function *getResults* gets executed.

In asynchronous programming (basically, allowing other operations to continue before one operation has completed - i.e. waiting for data in the database), callbacks are essential because we want to tell a function what to do once it’s done with a task.

``` js
function doSomethingAfterClick() {
  numberOfClicks++; // Count the number of mouse clicks, just for the sake of example.
}

const button = document.getElementById('action-button');

button.addEventListener("click", doSomethingAfterClick); // here is the callback situation

```

<p align="center">
  <img src="https://github.com/Liz2310/CLOUD-COMPUTING/blob/main/Assignments/Assignment4/images/ac.png">
</p>

In this image the concept of asynchronous becomes clearer:
- The parent doesn't need to wait for the callback function to return.
- An example of this is JavaScript:
	- You pass a function that will be invoked, but other events will continue to be processed until the callback is invoked (such as click of buttons). The order of the events doesn't matter, so the code is set to be listening for these events and execute callbacks untile said event happens.

In an API context this concept applies as follows:
- Asynchronous calls do not block (or wait) for the API call to return from the server. Execution continues on in the program, and when the call returns from the server, a "callback" function is executed.
- Asynchronous APIs can process multiple requests at the same time. The APIs allow time-consuming requests to be processed in the background while more minor requests are serviced right away.
- In JavaScript, if you add an `async` keyword to a script, JavaScript processes it in the background without stopping the execution of the following scripts. These APIs work in a similar fashion.
- These APIs are implemented using different protocols like WebHooks, Websockets, GraphQL Subscriptions, and Server-Sent Events. Like the OpenAPI specification, AsyncAPI provides a specification for Asynchronous APIs that allows developers, architects, and product managers to define asynchronous API interfaces.

## 4. Describe the concept of cold start in AWS Lambda. 

What is Serverless?
- Refers to serverless applications. 
- Serverless applications are ones that don’t need any server provision and do not require to manage servers.

What is AWS Lambda?
- Serverless computing platform provided by AWS.
- Therefore, there's no need to worry about which AWS resources to launch, or how they will be managed.
	- Instead, you put the code on Lambda, and it runs.

How AWS Lambda works:
- The code is executed based on the response to events in AWS services such as add/delete files in S3 bucket, HTTP request from Amazon API gateway, etc.
- It can only be used to execute background tasks.

<p align="center">
  <img src="https://github.com/Liz2310/CLOUD-COMPUTING/blob/main/Assignments/Assignment4/images/lambda.jpeg">
</p>

- **Step 1:** First upload your AWS Lambda code in any language supported by AWS Lambda. 

- **Step 2:** Some AWS services which allow you to trigger AWS Lambda.

- **Step 3:** AWS Lambda upload code and the event details on which it should be triggered.

- **Step 4:** Executes AWS Lambda Code when it is triggered by AWS services.

- **Step 5:** AWS charges only when the AWS lambda code executes, and not otherwise.

What is cold start in AWS Lambda?
- Lambda uses its own containers to execute code, these containers have predefined runtime environments.

- When a function is called for the very first time, Lambda will pick up an empty container with the appropriate runtime and wrap the function, already pulled from S3.
	- The first time a function is called, it takes a bit more time to execute and respond because of this setup. 
	- Any subsequent iteration with the same function will be quite faster than the first one.
- So the very first iteration with a function is called a **cold start**. 
	- When a new instance handles its first request, the response time increases 


## 5. Describe each HTTP methods. 15 points.

What is HTTP?
- Stands for **H**yper **T**ext **T**ransfer **P**rotocol.
- It's an application-layer protocol for exchanging files on the World Wide Web, such as HTML.
	- HTTP follows a typical client-server model, with web browsers being HTTP clients that send file requests to Web servers.

- Communication between client computers and web servers is done by sending **HTTP Requests** and receiving **HTTP Responses**

HTTP Methods:
- GET: used only to retrieve resource representation/information (read-only).
	- It's idempotent: making multiple identical requests must produce the same result every time until another method (POST or PUT) has changed the state of the resource on the server.

- HEAD: is similar to the GET method, but without the response body (transfers the status line and header section only).
	- It returns the headers that would be returned if the request was made with the GET method.
	- Example: a GET request could produce a large download, a HEAD request could read its *Content-Length* header to check the filesize without actually downloading the file.
	- It's also idempotent

- POST: creates a new resource on the server, causing a change in state or side effects on the server's side.
	- The request body carries the data to be created in the server.
	- It's not idempotent: it's not expected to get the same result every time a POST request is sent. For example making two identical POST requests will result in two different resources containing the same information (except resource ids).

- PUT: updates an existing resource by sending the updated data in the request body to the server.
	- The update is done by replacing the resource's content completely.
	- It's idempotent: making the same request once or several times successively has the same effect (that is no _side_ effect).

- DELETE: deletes all current representations of the target resource given by a URI.
	- It's idempotent: regardless of the number of calls, it returns the same result.

- CONNECT: used for making end-to-end connections between a client and a server (it creates a tunnel to the server identified by a given URI).
	- A use case example would be to safely transfer a large file between the client and the server.

- OPTIONS: to get information about the allowed HTTP methods for a given URL or an entire server (denoted by *). 
	- It's idempotent.

- TRACE: it creates a loop-back test with the same request body that the client sent to the server before.
	- The server echoes back the TRACE request it received, this way the user can see if during the transaction, the request was modified by proxies (it allows one to take a look at the path to the targeted resource/server; steps taken to deliver an HTTP request to the resource).
	- It's idempotent.
	- Potentially dangerous because it could reveal credentials used anywhere along the path to the targeted resource.

- PATCH: it applies partial modifications to a resource.
	- The PATCH method is the correct choice for partially updating an existing resource, and PUT should only be used if a resource is being replaced in its entirety.
		- PATCH is a set of instructions (which come in standard formats such as JSON or XML) on how to modify a resource, PUT is a complete representation of a resource.
	- Not necessarily idempotent, but it can be.

## 6. Describe how you can automate a deployment of a static website to S3. 15 points

Automating a website in an Amazon S3 bucket can de defined as a CI/CD pipeline (continuous integration and continuous delivery). 

According to AWS documentation, this can be done using GitHub as a source provider.

> The pipeline starts when new items are committed, and the changes are then reflected in the S3 bucket.

The pipeline is created via he **AWS Codepipeline** service.
- It's CD service used to automate the building, testing and deploying of software into production environment.
- In this case, changes made to the GitHub repository of the static website to AWS S3 will be automatically deployed.
- To create a pipeline, the cli command looks like this:
	 `aws codepipeline create-pipeline --pipeline`
	 
	The --pipeline flag points to a JSON file the attributes and values that indicate the actions and stages that the pipeline is going to perform.
	-	What's important to note in this JSON is the stages section, specifically the Source subsection.
		-	This is where the GitHub ()integration with AWS Codepipeline goes.
		-	This integration is created with the following command and format:
    `aws codestar-connections create-connection --provider-type GitHub --connection-name MyConnection`
    This returns the connection's ARN information, which is used in the pipeline's JSON:
    ```json
    {
    "Name": "Source",
    "Actions": [
        {
            "InputArtifacts": [],
            "ActionTypeId": {
                "Version": "1",
                "Owner": "AWS",
                "Category": "Source",
                "Provider": "CodeStarSourceConnection"
            },
            "OutputArtifacts": [
                {
                    "Name": "SourceArtifact"
                }
            ],
            "RunOrder": 1,
            "Configuration": {
                "ConnectionArn": "arn:aws:codestar-connections:region:account-id:connection/connection-id",
                "FullRepositoryId": "some-user/my-repo",
                "BranchName": "main",
                "OutputArtifactFormat": "CODE_ZIP"
            },
            "Name": "ApplicationSource"
        }
    ]
    },
   ```

	NOTE:  The GitHub repository should have the static website files.
- Once having the pipeline created., any changes made on the GitHub repository should be visible in the live URL.  

Observations:
- Made for read-only content (it's not safe for transaction with sensitive data; Amazon S3 uses HTTP protocol).

## 7. Read the Real-world [Engineering Challenges #8: Breaking up a Monolith](https://newsletter.pragmaticengineer.com/p/real-world-eng-8) article and write a summary and opinions about it. 10 points.

**Summary:**
- In 2019, Khan Academy took on the challenge of moving one million lines of Python code and splitting them across more than 40 services, but now in a different language: Go. This migration took 3.5 years and involved around 100 software engineers.
- The migration was triggered because of Python's 2 end.
- The team, after due diligence, decided to migrate to Go (quick compile times, good support on Google App Engine, saves memory, amongst other benefits).
- Goals of the project:
	-  Migrate 100% of Python 2 code to Go.
	- Have only GraphQL endpoints.
	- Use GraphQL federation.
	- Agree on architectural strategies (from monolith to services-oriented architecture).
		- Testing/deployments for a single services is way quicker.
		- Limited impact in case something goes wrong in a service.
		- Personalized configurations for each service.
- Two phases:
	- *Phase 1 Minimum Viable Experience:* Define what the key features were from a user experience perspective (content publishing, content delivery, progress tracking, user management, etc.), in order to prioritize their migration.
	- *Phase 2: endgame:* Rewriting everything else that wasn't part of the MVE, internal tools and adding extra features to services. 

- Gradual migration with gradual testing was the approach: Testing is key part of the migration. 
	- Simulating traffic in the new services.
	- Side by side testing of GraphQL queries on both services but only returning a response from the stable (Python) service.
	- Canary testing for modifying the server on the new Go service.
	- Finally using completely the Go service, but having the Python service in case it's needed.
	- Remove Python service completely.

- The services followed the rule that only one service could write a given piece of data. 
- The project followed a fixed deadline, no room for flexibility on deliverables.
	- The team applied “borderless engineering”, which consists of individuals floating from team to team for short periods of time, to help out on work when it’s necessary.
	- This was done in order to meet set deadlines, putting the project at risk was not an option.

- Both the MVE and the migration were done and deployed on the preestablished dates.

**Opinions:**
- Most of the improvements or changes are forced on a project rather than "self impulsed" (in this case the end of Python 2 forced the team to change).
- Having and MVE rather than an MVP (MV Product) helps to really put developers in the shoes of users and prioritize what their needs are, therefore making it clear what the most important and urgent services are.
- The incremental/gradual testing and migration strategy makes it effective for situations where a rollback is needed. This enables quick changes, and at the same time enables quick solutions.
- Also I haven't come in contact with side-by-side testing, but its use is very clear in this case because of the fact that two services were being compared. Feels like an immediate way of knowing when something's working the way it's supposed to.
- I like this very modular approach of one service owns a piece of data, it leaves no room for ambiguity or confusion about what the service handles. Preps the service so any fresh pair of eyes know what they're dealing with.
- Sometimes flexibility is a big impediment to meeting deadlines. Taking hard measures can do great things in the process of accomplish a goal.
- Borderless engineering is an interesting concept, similar to the Spotify model where members from squads can rotate if necessary.
	- From personal experience, with the right set of people, this can create an amazing cross functional team and knowledge transfers become way easier.

- Changing languages sometimes relies more on how quickly the engineers can adapt to it rather than the costs it saves (contrary to this case where costs were prioritized).
- I agree that motivation in workspaces were active learning is embraced. Trying to figure out and learning the in and outs of a new technology. The feeling of reward this brings (most of the time) is immeasurable.
