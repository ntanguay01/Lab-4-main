# Lab-4
Using REST Countries API for school Project/Lab. Use to get Countries and get information about them including name, borders/neighbors, regions, currency, language, and flag quiz.


## Issues
- Each neighbors counts as one API requests so China and its neighbors cost 14 API requests, need to fix limitation
- Only gets max 25 results from searching, need to fix that to get all available searches
- Fixed max 25 results problem by by requesting limit=100 and looping on meta.more
- Also refactored _get and meta and split it into _request
- EUR and English get many results (more than 25) so use pagination loop similar to region requests
- Used currencies.code and language.code as propety paths and got HTTP 404 errors
- Fixed by reading the Field reference and using currencies and languages directly instead
- Fetching the list through every round would quickly burn up the free 1,000 monthly requests
- To fix this we fetch it once then cache it into memory
- Since Terminal can't render pictures send link to for picture