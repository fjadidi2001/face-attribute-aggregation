1. Setup Redis and test connection.

2. Implement Face Detection Service:

a. Load MTCNN model.

b. For an input image, detect faces.

c. For each face, generate UUID, crop the face region, store in Redis (maybe as base64), log time.

3. Landmark Extraction Service:

a. Load Dlib's model.

b. Listen for new face entries in Redis.

c. For each face, load the image, detect landmarks, store in Redis, log time.

4. Age/Gender Service:

a. Load the CNN model(s).

b. Listen for face entries, process each to predict age and gender, store results in Redis, log time.

5. Aggregation Service:

a. Monitor Redis for faces that have landmarks, age, and gender data.

b. When all data is present, aggregate into JSON, save to file and Redis.

6. Implement logging in each service, capturing start and end times.

7. Test with sample images, check Redis data, logs, and output JSONs.
