import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, Image, Button } from 'react-native';
export default function LoginScreen() {
//* Aquí guardamos lo que el usuario escribe*
const [correo, setCorreo] = useState('');
const [password, setPassword] = useState('');
//* Esta función se ejecuta al presionar el botón*
const handleLogin = async () => {
//* Validación básica para no mandar cosas vacías*
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
//* Si el servidor responde con 200 OK*
if (response.ok) {
//* Te muestro los primeros caracteres del Token para confirmar que llegó*
Alert.alert("¡Éxito!", "Token recibido: " + data.token.substring(0, 15) + "...");
//* Más adelante, aquí guardaremos el token en el almacenamiento del celular*
} else {
//* Si mandas mala contraseña o el user no existe (Error 400/401)*
Alert.alert("Error", data.message || "Credenciales inválidas");
}
} catch (error) {
Alert.alert("Error de Conexión", "No se pudo conectar a Flask. Revisa que el servidor esté corriendo y la IP sea correcta.");
console.error(error);
}
};
return (
<View style={styles.containerMain}> 
  <View style={styles.container}>
    <Image source={require('./assets/images/medigestion.png')} style={styles.logo} />
    <Text style={styles.subtitle}>Inicia sesión para gestionar tus Citas</Text>
    <TextInput
      style={styles.input}
      placeholder="Correo electrónico"
      value={correo}
      onChangeText={setCorreo}
      keyboardType="email-address"
      autoCapitalize="none" //* Para que no ponga mayúscula inicial molesta*
    />
    <TextInput
      style={styles.input}
      placeholder="Contraseña"
      value={password}
      onChangeText={setPassword}
      secureTextEntry //* Esto oculta la contraseña con punticos*
    />
    <TouchableOpacity style={styles.button} onPress={handleLogin}>
    <Text style={styles.buttonText}>Ingresar</Text>
    </TouchableOpacity>
    <View style={styles.container2}>

    <Text style={styles.subtitle}>¿No tienes una Cuenta?</Text>
    <TouchableOpacity style={styles.button2}> 
      <Text style={styles.buttonText}>Registrarse</Text>
    </TouchableOpacity>

    <TouchableOpacity style={styles.button3}> 
      <Text style={{color: '#ff0000'}}>Olvidé mi contraseña</Text>
    </TouchableOpacity>
    
    </View>
  </View>
</View>
);
}
//* Estilos rápidos y limpios*
const styles = StyleSheet.create({
  containerMain: {
  flex: 1,
  justifyContent: 'center',
  padding: 20,
  backgroundColor: '#f4f6f8',
},
container: {
  flex: 1,
  justifyContent: 'center',
  padding: 20,
  backgroundColor: '#f4f6f8',
},
container2: {
  flex: 0,
  justifyContent: 'center',
  padding: 20,
  backgroundColor: '#f4f6f8',
},
title: {
  fontSize: 32,
  fontWeight: 'bold',
  textAlign: 'center',
  color: '',
  marginBottom: 10,
},
logo:{
  width: 285, 
  height: 130, 
  resizeMode:'container',
},
subtitle: {
  fontSize: 16,
  textAlign: 'center',
  color: '',
  marginBottom: 40,
  marginTop:20,
},
input: {
  backgroundColor: '',
  paddingHorizontal: 15,
  paddingVertical: 12,
  borderRadius: 8,
  borderWidth: 1,
  borderColor: '',
  marginBottom: 15,
  fontSize: 16,
},
button: {
  backgroundColor: '#28a745',
  padding: 15,
  borderRadius: 8,
  alignItems: 'center',
  marginTop: 10,
},
button2: {
  backgroundColor:'#007bff',
  title: '#fff',
  padding: 5,
  borderRadius: 8,
  alignItems: 'center',
  alignSelf:'center',
},
button3: {
  backgroundColor:'#f4f6f8',
  padding: 5,
  borderRadius: 8,
  alignItems: 'center',
  marginTop:20,
},
buttonText: {
  color: '#fff',
  fontSize: 18,
  fontWeight: 'bold',
},
});

