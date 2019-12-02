from routes import app, system

if __name__ == '__main__':
    app.run(debug=True)

print("Saving data...")
system.save_data()
print("Save complete")
