import React, { useState, useEffect } from 'react';
import { View, Text, Button, Image, ActivityIndicator, StyleSheet } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Speech from 'expo-speech';
import { io } from 'socket.io-client';

const socket = io('http://192.168.219.105:5001');

const HomeScreen = () => {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [image, setImage] = useState(null);

  useEffect(() => {
    socket.on('connect', () => {
      console.log('소켓 연결됨');
    });

    socket.on('result', (data) => {
      setLoading(false);
      setResult(data.result);
      Speech.speak(`감지된 객체는 ${data.result}입니다`);
    });

    return () => {
      socket.off('connect');
      socket.off('result');
    };
  }, []);

  const pickImage = async () => {
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permissionResult.granted) {
      alert('사진 접근 권한이 필요합니다!');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: false,
      base64: true,
    });

    if (!result.canceled && result.assets.length > 0) {
      const selectedImage = result.assets[0];
      setImage(selectedImage.uri);
      return selectedImage.base64;
    }

    return null;
  };

  const handleDetect = async () => {
    const base64Image = await pickImage();
    if (!base64Image) return;

    setLoading(true);
    socket.emit('image', { image: base64Image });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>YOLOv5 객체 인식 (WebSocket)</Text>
      <Button title="이미지 선택 후 객체 인식" onPress={handleDetect} />
      {image && <Image source={{ uri: image }} style={{ width: 200, height: 200, marginTop: 10 }} />}
      {loading && <ActivityIndicator size="large" />}
      <Text style={styles.resultText}>{result}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 24, marginBottom: 20 },
  resultText: { fontSize: 18, marginTop: 20 },
});

export default HomeScreen;
