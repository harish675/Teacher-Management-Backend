# Docker Deployment Import Fix

## Problem

When deploying to Render using Docker, the application failed with the following error:

```
ModuleNotFoundError: No module named 'src.lib'
```

This occurred because the codebase had **inconsistent import patterns**. Some files used absolute imports (`from src.lib.database`) while the Docker container's module resolution expected relative imports.

## Root Cause

The issue stems from how Python resolves module imports in different contexts:

- **Local Development**: When running `fastapi dev main.py`, the `main.py` adds the project root to `sys.path`, allowing absolute imports like `from src.lib.database` to work.

- **Docker Container**: When running `uvicorn src.app:app` directly, Python doesn't have the project root in `sys.path` the same way, so absolute imports starting with `src.` fail.

## Solution

Changed all absolute imports to **relative imports** in the following files:

### Files Modified

1. **`src/modules/student/student_router.py`**
   - Changed: `from src.lib.database import mongo_connection`
   - To: `from ...lib.database import mongo_connection`

2. **`src/modules/teacher/teacher_router.py`**
   - Changed: `from src.lib.database import mongo_connection`
   - To: `from ...lib.database import mongo_connection`

3. **`src/modules/course/course_router.py`**
   - Changed: `from src.lib.database import mongo_connection`
   - To: `from ...lib.database import mongo_connection`

4. **`src/modules/assign_teacher/assign_teacher_router.py`**
   - Changed: `from src.lib.database import mongo_connection`
   - To: `from ...lib.database import mongo_connection`

5. **`src/modules/enrolled_studets/enrolled_students_router.py`**
   - Changed: `from src.lib.database import mongo_connection`
   - To: `from ...lib.database import mongo_connection`

6. **`src/modules/seed_data/seed_data.py`**
   - Changed: `from src.lib.database import mongo_connection`
   - To: `from ...lib.database import mongo_connection`

## Understanding Relative Imports

The `...` in the import statement means:
- `.` = current package
- `..` = parent package
- `...` = grandparent package

For example, from `src/modules/student/student_router.py`:
- `...lib` goes up 3 levels: `student` → `modules` → `src`, then accesses `lib`

## Next Steps

1. **Commit and push** these changes to your Git repository
2. **Redeploy** on Render - the deployment should now succeed
3. The application will work both locally and in Docker

## Verification

After redeploying, you should see:
- ✅ Docker build completes successfully
- ✅ Application starts without import errors
- ✅ All API endpoints are accessible

## Prevention

To avoid this issue in the future:
- **Use relative imports** for internal package imports
- **Use absolute imports** only for external packages (like `fastapi`, `pymongo`, etc.)
- Test with `uvicorn src.app:app` locally before deploying
