//Importaciones de React
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Image } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useNavigation } from '@react-navigation/native';

import { GlobalStyles } from '../../assests/theme/globalStyles.js';

//Importaciones Locales

export default function ScreenLoading() {
  const estado = x;
  return (
    <View>
      <Text style={GlobalStyles.subtittle}>Ingresando...</Text>
    </View>
  );
}
