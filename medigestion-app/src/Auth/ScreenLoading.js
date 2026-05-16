//Importaciones de React
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  Image,
  Alert,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useNavigation } from '@react-navigation/native';

//Importaciones Locales

import { GlobalStyles } from '../../assets/theme/globalStyles.js';

// Archivo con la verificacion del token
import { verificarToken } from '../../components/token_requerido.js';
import { datosUsuario } from '../../components/datosUsuario.js';

export default function ScreenLoading() {
  const { autorizado, cargando } = verificarToken();
  const navigation = useNavigation();
  const perfil = datosUsuario();

  const redireccion = () => {
    if (perfil.rol == 'pacientes') {
      navigation.replace('MainPaciente');
    } else if (perfil.rol == 'admintb') {
      Alert.alert('Pantalla de Admin aún no creada');
      navigation.replace('Login');
    } else {
      Alert.alert('Pantalla de Medico aún no creada');
      navigation.replace('Login');
    }
  };

  useEffect(() => {
    if (!cargando && !autorizado) {
      Alert.alert(
        'Sesión Expirada',
        'No tienes permiso o tu sesión terminó. Por favor inicia sesión de nuevo.',
        [
          {
            text: 'OK',
            onPress: () => navigation.replace('Login'),
          },
        ],
        { cancelable: false }, // Evita que cierre la alerta tocando por fuera
      );
    } else if (autorizado && perfil) {
      redireccion();
    }
  }, [cargando, autorizado, navigation, perfil]);

  return (
    <View
      style={[
        GlobalStyles.container,
        { alignItems: 'center', justifyContent: 'center' },
      ]}
    >
      <Image
        source={require('../../assets/images/medigestion.png')}
        style={[GlobalStyles.logo, { marginBottom: 20 }]}
      />
      <Text style={GlobalStyles.tittle}>Ingresando...</Text>
    </View>
  );
}
