
import 'package:flutter/material.dart';

void main() {
  runApp(GenesisApp());
}

class GenesisApp extends StatelessWidget {

  @override
  Widget build(BuildContext context) {

    return MaterialApp(

      title: 'Genesis Mobile',

      home: Scaffold(

        appBar: AppBar(
          title: Text('Genesis AI Workstation'),
        ),

        body: Center(
          child: Text(
            'Genesis Online 🧬'
          ),
        ),

      ),

    );

  }
}
