import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';

export default function LoginScreen() {
  // Aquí guardamos lo que el usuario escribe
  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');

  // Esta función se ejecuta al presionar el botón
  const handleLogin = async () => {
    // Validación básica para no mandar cosas vacías
    if (!correo || !password) {
      Alert.alert("Error", "Por favor llena todos los campos");
      return;
    }

    try {
      const urlServidor = 'http://192.168.2.5:5000/api/login'; 

      const response = await fetch(urlServidor, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          correo: correo,
          password: password
        }),
      });

      const data = await response.json();

      // Si el servidor responde con 200 OK
      if (response.ok) {
        // Te muestro los primeros caracteres del Token para confirmar que llegó
        Alert.alert("¡Éxito!", "Token recibido: " + data.token.substring(0, 15) + "...");
        
        // Más adelante, aquí guardaremos el token en el almacenamiento del celular
      } else {
        // Si mandas mala contraseña o el user no existe (Error 400/401)
        Alert.alert("Error", data.message || "Credenciales inválidas");
      }
    } catch (error) {
      Alert.alert("Error de Conexión", "No se pudo conectar a Flask. Revisa que el servidor esté corriendo y la IP sea correcta.");
      console.error(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Medigestión</Text>
      <Text style={styles.subtitle}>Inicia sesión para continuar</Text>

      <TextInput
        style={styles.input}
        placeholder="Correo electrónico"
        value={correo}
        onChangeText={setCorreo}
        keyboardType="email-address"
        autoCapitalize="none" // Para que no ponga mayúscula inicial molesta
      />

      <TextInput
        style={styles.input}
        placeholder="Contraseña"
        value={password}
        onChangeText={setPassword}
        secureTextEntry // Esto oculta la contraseña con punticos
      />

      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Entrar</Text>
      </TouchableOpacity>
    </View>
  );
}

// Estilos rápidos y limpios
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#2c3e50',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    color: '#7f8c8d',
    marginBottom: 40,
  },
  input: {
    backgroundColor: '#fff',
    paddingHorizontal: 15,
    paddingVertical: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ddd',
    marginBottom: 15,
    fontSize: 16,
  },
  button: {
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});