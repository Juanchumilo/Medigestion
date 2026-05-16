import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  Image,
  Button,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

//Import de funciones adicionales
import { GlobalStyles } from '../../assets/theme/globalStyles.js';

export default function LoginScreen({ navigation }) {
  //* Aquí guardamos lo que el usuario escribe*
  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');
  //* Esta función se ejecuta al presionar el botón*
  const handleLogin = async () => {
    //* Validación básica para no mandar cosas vacías*
    if (!correo || !password) {
      Alert.alert('Error', 'Por favor llena todos los campos');
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
          password: password,
        }),
      });

      const data = await response.json();

      //* Si el servidor responde con 200 OK*
      if (response.ok) {
        //Guardamos la informacion que trae Flask
        await AsyncStorage.setItem('token_usuario', data.token);
        // data.datos es un objeto, asi que lo cambiamos a string
        await AsyncStorage.setItem('datos_usuario', JSON.stringify(data.datos));

        navigation.replace('ScreenLoading');
      } else {
        //* Si manda mal la contraseña o el user no existe (Error 400/401)*
        Alert.alert('Error', data.message || 'Credenciales inválidas');
      }
    } catch (error) {
      //* Si el try da error
      Alert.alert(
        'Error de Conexión',
        'No se pudo conectar a Flask. Revisa que el servidor esté corriendo y la IP sea correcta.',
      );
      console.error(error);
    }
  };

  return (
    <View style={[GlobalStyles.container]}>
      <View style={[GlobalStyles.container]}>
        <Image
          source={require('../../assets/images/medigestion.png')}
          style={[GlobalStyles.logo]}
        />
        <Text style={[GlobalStyles.subtitle, { marginBottom: 20 }]}>
          Inicia sesión para gestionar tus Citas Médicas
        </Text>
        <TextInput
          style={[GlobalStyles.input]}
          placeholder='Correo electrónico'
          value={correo}
          onChangeText={setCorreo}
          keyboardType='email-address'
          autoCapitalize='none' //* Para que no ponga mayúscula inicial molesta*
        />
        <TextInput
          style={[GlobalStyles.input]}
          placeholder='Contraseña'
          value={password}
          onChangeText={setPassword}
          secureTextEntry //* Esto oculta la contraseña con punticos*
        />
        <TouchableOpacity
          style={[GlobalStyles.buttonMain]}
          onPress={handleLogin}
        >
          <Text style={[GlobalStyles.textbutton]}>Ingresar</Text>
        </TouchableOpacity>
        <View style={[GlobalStyles.container]}>
          <Text
            style={[
              GlobalStyles.subtitle,
              { marginBottom: 40, marginTop: 20, color: '' },
            ]}
          >
            ¿No tienes una Cuenta?
          </Text>
          <TouchableOpacity style={styles.button2}>
            <Text style={[GlobalStyles.textbutton]}>Registrarse</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.button3}>
            <Text style={{ color: '#ff0000' }}>Olvidé mi contraseña</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

//* Estilos adicionales
const styles = StyleSheet.create({
  button2: {
    backgroundColor: '#007bff',
    title: '#fff',
    padding: 5,
    borderRadius: 8,
    alignItems: 'center',
    alignSelf: 'center',
  },
  button3: {
    backgroundColor: '#f4f6f8',
    padding: 5,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 30,
  },
});
