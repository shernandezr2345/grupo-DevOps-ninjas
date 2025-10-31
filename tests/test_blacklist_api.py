import pytest
from app.models import BlacklistModel
from app.extensions import db

class TestBlacklistAPI:

    def test_add_email_success(self, client, init_database, auth_headers):
        """
        Prueba el caso de éxito para agregar un nuevo email a la lista negra.
        Verifica el código de estado 201 y el mensaje de éxito.
        También verifica que el registro fue realmente creado en la base de datos.
        """
        payload = {
            "email": "test.success@example.com",
            "app_uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "blocked_reason": "User requested to be blocked"
        }

        response = client.post('/blacklists', json=payload, headers=auth_headers)

        assert response.status_code == 201
        assert response.json['message'] == "Email added to blacklist error"

        entry = BlacklistModel.query.filter_by(email=payload['email']).first()
        assert entry is not None
        assert entry.app_uuid == payload['app_uuid']
        assert entry.blocked_reason == payload['blocked_reason']


    def test_get_existing_email_returns_found(self, client, init_database, auth_headers):
        """
        Prueba el caso de éxito para obtener un email que existe en la lista negra.
        Verifica el código de estado 200 y que la respuesta indica que está en la lista.
        """
        email_to_find = "find.me@example.com"
        reason = "Reason for testing GET"
        
        new_entry = BlacklistModel(
            email=email_to_find,
            app_uuid="some-uuid-for-get-test",
            blocked_reason=reason,
            source_ip="127.0.0.1"
        )
        db.session.add(new_entry)
        db.session.commit()

        response = client.get(f'/blacklists/{email_to_find}', headers=auth_headers)


        assert response.status_code == 200
        response_data = response.json
        assert response_data['is_blacklisted'] is True
        assert response_data['reason'] == reason
    
    def test_add_duplicate_email_fails(self, client, init_database, auth_headers):
        """
        Prueba que la API rechaza correctamente un intento de agregar un email duplicado.
        Verifica el código de estado 409 Conflict.
        """
        payload = {
            "email": "duplicate.email@example.com",
            "app_uuid": "some-uuid"
        }
        response1 = client.post('/blacklists', json=payload, headers=auth_headers)
        assert response1.status_code == 201

        response2 = client.post('/blacklists', json=payload, headers=auth_headers)

        assert response2.status_code == 409
        assert response2.json['message'] == "Email already exists in the blacklist"

    def test_add_email_with_invalid_format_fails(self, client, init_database, auth_headers):
        """
        Prueba que la API rechaza un email con formato inválido.
        Verifica el código de estado 400 Bad Request y el mensaje de error específico.
        """
        payload = {
            "email": "not-a-valid-email",
            "app_uuid": "some-uuid"
        }

        response = client.post('/blacklists', json=payload, headers=auth_headers)

        assert response.status_code == 400
        assert 'email' in response.json
        assert response.json['email'][0] == "Not a valid email address."

    def test_add_email_with_missing_required_field_fails(self, client, init_database, auth_headers):
        """
        Prueba que la API rechaza una petición a la que le falta un campo requerido (app_uuid).
        Verifica el código de estado 400 Bad Request.
        """
        payload = {
            "email": "missing.field@example.com"
            # Falta el campo "app_uuid"
        }

        response = client.post('/blacklists', json=payload, headers=auth_headers)

        assert response.status_code == 400
        assert 'app_uuid' in response.json
        assert response.json['app_uuid'][0] == "Missing data for required field."

    def test_get_non_existing_email_returns_not_found(self, client, init_database, auth_headers):
        """
        Prueba que la API responde correctamente al consultar un email que no existe.
        Verifica el código de estado 200 y que la respuesta indica que no está en la lista.
        """
        email_to_check = "non.existent@example.com"

        response = client.get(f'/blacklists/{email_to_check}', headers=auth_headers)

        assert response.status_code == 200
        assert response.json['is_blacklisted'] is False
    
    def test_access_protected_endpoint_without_token_fails(self, client, init_database):
        """
        Prueba que un endpoint protegido devuelve 401 Unauthorized si no se proporciona un token.
        Nótese que esta prueba NO usa la fixture 'auth_headers'.
        """
        payload = {
            "email": "unauthorized.access@example.com",
            "app_uuid": "some-uuid"
        }

        response = client.post('/blacklists', json=payload) # Sin cabeceras de autorización

        assert response.status_code == 401
        assert 'msg' in response.json
        assert response.json['msg'] == "Missing Authorization Header"

    def test_health_endpoint_returns_ok(self, client):
        """
        Prueba que el endpoint de salud (/health) es accesible y devuelve el estado correcto.
        Este endpoint no necesita base de datos ni autenticación.
        """
        response = client.get('/health')

        assert response.status_code == 200
        response_data = response.json
        assert response_data['status'] == 'ok'
        assert response_data['message'] == 'API is running'
        assert response_data['database_status'] == 'ok'

    def test_get_token_endpoint_returns_token(self, client):
        """
        Prueba que el endpoint de generación de tokens (/get-token) funciona correctamente.
        """
        response = client.get('/get-token')
        
        assert response.status_code == 200
        response_data = response.json
        assert 'access_token' in response_data
        assert isinstance(response_data['access_token'], str)
