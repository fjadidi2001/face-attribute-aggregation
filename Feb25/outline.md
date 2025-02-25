1. Face Detection Service: Takes an image, uses MTCNN/YOLO to detect faces. For each face, extract the bounding box and assign a UUID. Store the face images or coordinates in Redis with the UUID.

2. Landmark Extraction Service: For each face detected, get the face image from Redis, apply Dlib's 68-point model, extract landmarks. Store the landmarks in Redis under the same UUID.

3. Age/Gender Estimation Service: For each face, retrieve the face image, run through the CNN model(s), predict age group and gender. Store results in Redis.

4. Aggregation Service: Once all data (landmarks, age, gender) is available for a UUID, aggregate into a JSON object and save to a file. Also, store the JSON in Redis for quick access.


