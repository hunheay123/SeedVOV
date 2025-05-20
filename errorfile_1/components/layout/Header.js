//import React from "react";
//import {
//  View,
//  Text,
//  StyleSheet,
//  TouchableOpacity,
//  SafeAreaView,
//} from "react-native";
//import { Ionicons } from "@expo/vector-icons";
//
//const Header = () => {
//  return (
//    <SafeAreaView style={styles.safeArea}>
//      <View style={styles.headerContainer}>
//        {/* 설정 아이콘 */}
//        <TouchableOpacity onPress={() => console.log("설정 버튼 눌림")}>
//          <Ionicons name="settings-outline" size={24} color="black" />
//        </TouchableOpacity>
//
//        {/* 화면 이름 텍스트 */}
//        <View style={styles.titleContainer}>
//          <Text style={styles.title}>Home</Text>
//          <Text style={styles.title}>OCR</Text>
//        </View>
//
//        {/* 오른쪽 공간을 비워서 정렬 맞춤 */}
//        <View style={{ width: 24 }} />
//      </View>
//    </SafeAreaView>
//  );
//};

//const styles = StyleSheet.create({
//  safeArea: {
//    backgroundColor: "#fff",
//  },
//  headerContainer: {
//    height: 50,
//    flexDirection: "row",
//    alignItems: "center",
//    justifyContent: "space-between",
//    paddingHorizontal: 16,
//    borderBottomWidth: 1,
//    borderColor: "#ddd",
//  },
//  titleContainer: {
//    flexDirection: "row",
//    gap: 12,
//  },
//  title: {
//    fontSize: 18,
//    fontWeight: "bold",
//  },
//});

// export default Header;
