---
name: app-manager
description: Manage the lifecycle of the To-Do and Budget Manager application. Use when the application needs to be started, stopped, or restarted to apply changes or troubleshoot.
---

# App Manager Skill

This skill provides a centralized way to manage the `todo_app.py` process.

## Workflows

### Restarting the App
To restart the app after making code changes:
1. Run the management script with the `restart` argument.
2. Verify the status.

Example:
```bash
bash scripts/manage_app.sh restart
```

### Stopping the App
To stop the app when it's no longer needed:
```bash
bash scripts/manage_app.sh stop
```

### Starting the App
To start the app:
```bash
bash scripts/manage_app.sh start
```

### Checking Status
To check if the app is currently running:
```bash
bash scripts/manage_app.sh status
```

## Resources
- `scripts/manage_app.sh`: Bash script that handles process management using `fuser` and `python`.
