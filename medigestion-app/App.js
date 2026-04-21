// App.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// Importas tus habitaciones (src)
import Login from './src/Login';
import Paciente from './src/Paciente';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      {/* initialRouteName define qué src carga primero */}
      <Stack.Navigator initialRouteName="Login">
        
        {/* Aquí registras tus src */}
        <Stack.Screen 
          name="Login" 
          component={Login} 
          options={{ headerShown: false }} // Esto oculta la barra superior fea
        />
        <Stack.Screen 
          name="Paciente" 
          component={Paciente} 
          options={{ title: 'Apartado Paciente' }} // Título de la barra superior
        />

      </Stack.Navigator>
    </NavigationContainer>
  );
}