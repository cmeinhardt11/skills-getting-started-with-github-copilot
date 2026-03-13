import src.app as app_module


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "temporary.student@mergington.edu"
    app_module.activities[activity_name]["participants"].append(email)

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "temporary.student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_not_found_for_non_member(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unregister_removes_all_duplicate_entries_for_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"
    app_module.activities[activity_name]["participants"].extend([email, email])

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    remaining = app_module.activities[activity_name]["participants"]
    assert email not in remaining
