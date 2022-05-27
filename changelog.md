# 12.05.2022
Moved from in-memory db to file. Changed honkai and homeline logic - now it filters by 'honkai=True/False', not by source. Moved 'unique' to separate file. Refactored 'update' as a background task. Choose axios base url basen on whether it's 'npm run serve' or 'build'.

# 13.05.2022
Updated .env.example file. Nginx.

# 16.05.2022
Set up nginx. Made a little clean up.

# 20.05.2022
Added user system on the frontend.

# 23.05.2022
Routes guard. Token cookie auth. Display pixiv images without referer extentions. Pixiv embeds. Dropdown collapse.

# 24.05.2022
Separated routers. Dropped "/api" in embed url.

# 25.05.2022
Async requests. Returned "/api" in embed url

# 26.05.2022
Adjusted pixiv embeds 'big' logic. Added feature to request pic with arbitrary number.

# 27.05.2022
Type validations in request.py