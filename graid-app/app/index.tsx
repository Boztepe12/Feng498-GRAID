import React, { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  ActivityIndicator,
  Alert,
  Animated,
} from 'react-native';

const App = () => {
  interface SensorData {
    soilMoisture: string;
    humidity: string;
    temperature: string;
    ec: string;
    ph: string;
    nitrogen: string;
    phosphorous: string;
    potassium: string;
  }
  
  const [sensorData, setSensorData] = useState<SensorData | null>(null);
  const [isRealData, setIsRealData] = useState(false);
  const [loading, setLoading] = useState(true);
  // serverStatus true ise sunucuya istek gönderildi, false ise gönderilemedi.
  const [serverStatus, setServerStatus] = useState<boolean | null>(null);

  // Her iki gösterge için ayrı Animated.Value'lar
  const sensorBlinkAnim = useRef(new Animated.Value(1)).current;
  const serverBlinkAnim = useRef(new Animated.Value(1)).current;

  // Verilen animasyon değeri için yanıp sönen animasyonu başlatan fonksiyon
  const startBlinking = (animValue: Animated.Value) => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(animValue, {
          toValue: 0,
          duration: 500,
          useNativeDriver: true,
        }),
        Animated.timing(animValue, {
          toValue: 1,
          duration: 500,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  // Sensör verilerini ESP'den çekip, sunucuya gönderme işlemini yapan fonksiyon
  const sendDataToServer = async (data: SensorData) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/myapp/start', {
        method: 'GET',
      });
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }
      setServerStatus(true);
    } catch (error) {
      console.error('Sunucuya veri gönderilemedi:', error);
      setServerStatus(false);
    } finally {
      startBlinking(serverBlinkAnim);
    }
  };

  useEffect(() => {
    const fetchSensorData = async () => {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => {
        controller.abort();
      }, 5000);

      try {
        const response = await fetch('http://your-esp-endpoint/sensor', {
          signal: controller.signal,
        });
        clearTimeout(timeoutId);
        if (!response.ok) {
          throw new Error(`HTTP Hatası: ${response.status}`);
        }
        const data = await response.json();
        setSensorData(data);
        setIsRealData(true);
      } catch (error) {
        console.error('Sensör verileri çekilemedi:', error);
        Alert.alert(
          'Veri Çekme Hatası',
          'Sensör verilerine ulaşılamıyor. Dummy veriler kullanılacak.',
          [{ text: 'Tamam' }]
        );
        const dummyData: SensorData = {
          soilMoisture: '35%',
          humidity: '41%',
          temperature: '22°C',
          ec: '1.2 mS/cm',
          ph: '6.8',
          nitrogen: '20 mg/kg',
          phosphorous: '15 mg/kg',
          potassium: '25 mg/kg',
        };
        setSensorData(dummyData);
        setIsRealData(false);
      } finally {
        setLoading(false);
      }
    };

    fetchSensorData();
  }, []);

  useEffect(() => {
    if (sensorData) {
      startBlinking(sensorBlinkAnim);
      sendDataToServer(sensorData);
    }
  }, [sensorData]);

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Veriler Yükleniyor...</Text>
      </View>
    );
  }

  if (!sensorData) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Sensör verisi bulunamadı.</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {/* ESP verisinin durumu için gösterge */}
      <Animated.View
        style={[
          styles.blinkingBox,
          { 
            opacity: sensorBlinkAnim, 
            backgroundColor: isRealData ? 'green' : 'red' 
          },
        ]}
      >
        <Text style={styles.blinkingText}>
          {isRealData ? "ESP'den Gerçek Veri Geldi!" : "ESP'den Veri Gelmedi"}
        </Text>
      </Animated.View>
      {/* Sunucuya istek gönderim durumu için gösterge */}
      <Animated.View
        style={[
          styles.blinkingBox,
          { 
            opacity: serverBlinkAnim, 
            backgroundColor: serverStatus ? 'green' : 'red' 
          },
        ]}
      >
        <Text style={styles.blinkingText}>
          {serverStatus ? "Sunucuya İstek Gönderildi!" : "Sunucuya İstek Gönderilemedi!"}
        </Text>
      </Animated.View>
      <Text style={styles.header}>Sensör Verileri</Text>
      <View style={styles.item}>
        <Text style={styles.label}>Soil Moisture:</Text>
        <Text style={styles.value}>{sensorData.soilMoisture}</Text>
      </View>
      <View style={styles.item}>
        <Text style={styles.label}>Humidity:</Text>
        <Text style={styles.value}>{sensorData.humidity}</Text>
      </View>
      <View style={styles.item}>
        <Text style={styles.label}>Temperature:</Text>
        <Text style={styles.value}>{sensorData.temperature}</Text>
      </View>
      <View style={styles.item}>
        <Text style={styles.label}>Electric Conductivity (EC):</Text>
        <Text style={styles.value}>{sensorData.ec}</Text>
      </View>
      <View style={styles.item}>
        <Text style={styles.label}>pH:</Text>
        <Text style={styles.value}>{sensorData.ph}</Text>
      </View>
      <View style={styles.item}>
        <Text style={styles.label}>Nitrogen:</Text>
        <Text style={styles.value}>{sensorData.nitrogen}</Text>
      </View>
      <View style={styles.item}>
        <Text style={styles.label}>Phosphorous:</Text>
        <Text style={styles.value}>{sensorData.phosphorous}</Text>
      </View>
      <View style={styles.item}>
        <Text style={styles.label}>Potassium:</Text>
        <Text style={styles.value}>{sensorData.potassium}</Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    alignItems: 'stretch',
    backgroundColor: '#F5FCFF',
    flexGrow: 1,
  },
  header: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#333',
  },
  blinkingBox: {
    padding: 8,
    borderRadius: 5,
    alignSelf: 'center',
    marginBottom: 10,
  },
  blinkingText: {
    color: '#fff',
    fontWeight: 'bold',
    textAlign: 'center',
  },
  item: {
    backgroundColor: '#FFFFFF',
    padding: 10,
    marginBottom: 8,
    borderRadius: 8,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  label: {
    fontSize: 16,
    color: '#555',
  },
  value: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#007AFF',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 18,
    color: 'red',
    textAlign: 'center',
  },
});

export default App;
