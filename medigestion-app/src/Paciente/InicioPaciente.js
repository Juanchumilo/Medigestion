import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  Image,
  TouchableOpacity,
  Alert,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useNavigation } from '@react-navigation/native';

// Importar Funciones adicionales
import CreadorCitas from '../../components/CreadorCitas.js';
import BuscadorCitas from '../../components/BuscadorCitas.js';
import { datosUsuario } from '../../components/datosUsuario.js';
import { capitalizarNombre } from '../../utils/toUpperCase.js';
import { GlobalStyles } from '../../assets/theme/globalStyles.js';
// Funcion para verificar el token
import { verificarToken } from '../../components/token_requerido.js';

export default function InicioPaciente() {
  const [vistaActiva, setVistaActiva] = useState('inicio');
  const perfil = datosUsuario(); // Funcion creada para recibir los datos del Usuario
  const { autorizado, cargando } = verificarToken();
  const navigation = useNavigation();

  useEffect(() => {
    if (!cargando && !autorizado) {
      Alert.alert(
        'Sesión Expirada',
        'No tienes permiso o tu sesión terminó. Por favor inicia sesión de nuevo.',
        [
          {
            text: 'OK',
            // El replace ocurre ÚNICAMENTE cuando el usuario presiona el botón
            onPress: () => navigation.replace('Login'),
          },
        ],
        { cancelable: false }, // Evita que cierre la alerta tocando por fuera
      );
    }
  }, [cargando, autorizado, navigation]);

  if (cargando) {
    return (
      <View
        style={[
          GlobalStyles.container,
          { justifyContent: 'center', alignItems: 'center' },
        ]}
      >
        <Text style={styles.textoWelcome}>Ingresando...</Text>
      </View>
    );
  }

  if (!autorizado) {
    return <View style={GlobalStyles.container}></View>;
  }

  const renderizarVista = () => {
    if (vistaActiva === 'crear') {
      return <CreadorCitas />;
    }
    if (vistaActiva === 'buscar') {
      return <BuscadorCitas />;
    }
    // Default view
    return (
      <Text style={styles.textoWelcome}>Bienvenido a tu panel de Paciente</Text>
    );
  };

  return (
    <View style={[GlobalStyles.container, { alignItems: 'center' }]}>
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
        <Text style={styles.textoWelcome}>
          Hola, {capitalizarNombre(perfil?.nombre)}
        </Text>
        <Text style={styles.subtitle}>¿Qué deseas hacer el día de hoy?</Text>

        {/* The Navigation Buttons */}
        <View style={styles.container2}>
          <TouchableOpacity
            style={[
              GlobalStyles.buttonMain,
              { marginTop: 10, marginBottom: 24 },
            ]}
            onPress={() => setVistaActiva('crear')}
          >
            <Text style={[GlobalStyles.textbutton]}>Crear Cita</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[GlobalStyles.buttonMain]}
            onPress={() => setVistaActiva('buscar')}
          >
            <Text style={[GlobalStyles.textbutton]}>Consultar Citas</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container2: {
    color: '#e6e7e8',
    padding: 10,
    marginTop: 20,
  },

  textoWelcome: {
    fontSize: 20,
    fontWeight: 'bold',
  },
});
