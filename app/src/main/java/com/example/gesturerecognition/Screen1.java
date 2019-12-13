package com.example.gesturerecognition;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

public class Screen1 extends AppCompatActivity implements AdapterView.OnItemSelectedListener {

    private boolean mSpinnerInitialized = false;
    String[] gesturesArray = {"", "gift", "car", "pay", "pet", "sell", "explain", "that", "book", "now", "work", "total",
            "trip", "future", "good", "thank you", "learn", "should", "like", "movie","agent"};
    // Storage Permissions
    private static final int REQUEST_EXTERNAL_STORAGE = 1;
    private static String[] PERMISSIONS_STORAGE = {
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
    };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.screen1);
        verifyPermissions();
        Spinner spin = findViewById(R.id.spinner);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, gesturesArray);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spin.setAdapter(adapter);
        spin.setOnItemSelectedListener(this);
    }

    public void onItemSelected(AdapterView<?> arg0, View arg1, int position, long id) {
        if (!mSpinnerInitialized) {
            mSpinnerInitialized = true;
            return;
        }
        if (position != 0) {
            Intent intent = new Intent(this, Screen2.class);
            intent.putExtra("GESTURE_ID", gesturesArray[position]);
            startActivity(intent);
        }
    }

    @Override
    public void onNothingSelected(AdapterView<?> adapterView) {

    }

    // Required for API 23+
    public void verifyPermissions() {
        // Check if we have write permission
        int permission = ActivityCompat.checkSelfPermission(Screen1.this, Manifest.permission.WRITE_EXTERNAL_STORAGE);

        if (permission != PackageManager.PERMISSION_GRANTED) {
            // We don't have permission so prompt the user
            ActivityCompat.requestPermissions(
                    Screen1.this,
                    PERMISSIONS_STORAGE,
                    REQUEST_EXTERNAL_STORAGE
            );
        }
    }

}
