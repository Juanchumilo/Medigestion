// App.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

// Se Importan las plantillas (src)
import Login from './src/Auth/Login';
import InicioPaciente from './src/Paciente/InicioPaciente';
import ListaMedicos from './src/Paciente/ListaMedicos';
import EditarDatos from './src/Paciente/EditarDatos';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

// Esta es la barra de abajo
function MisTabs() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false }}>
      <Tab.Screen name='Inicio' component={InicioPaciente} />
      <Tab.Screen name='Medicos' component={ListaMedicos} />
      <Tab.Screen name='Datos' component={EditarDatos} />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName='Login'>
        <Stack.Screen
          name='Login'
          component={Login}
          options={{ headerShown: false }}
        />
        {/* Cuando el login sea exitoso, navegamos a 'MainApp' */}
        <Stack.Screen
          name='MainApp'
          component={MisTabs}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
