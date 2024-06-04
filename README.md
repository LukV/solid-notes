# Solid Notes

## Description

This project is a proof-of-concept "Notes" application for writing notes to Solid Pods. Solid (Social Linked Data) is a web decentralization project led by Sir Tim Berners-Lee. Solid Pods are personal online data stores where users can store their data securely and give granular access to applications and other users. By storing your notes in a pod they are no longer locked in to yer OneNote, Evernote, Notes, Notion. Yippie!

## Installation frontend

1. Clone the repository:
    ```
    git clone https://github.com/LukV/solid-notes.git
    ```

2. Install dependencies:
    ```
    cd notes-app
    npm install
    ```

3. Start the development server:
    ```
    npm run dev
    ```

## Installation backend

1. Install Python dependencies:
    ```
    cd backend
    pip install -r requirements.txt
    ```

2. Run the server:
    ```
    uvicorn app.main:app --reload
    ```

## Contributing

This project is a proof-of-concept and is not currently accepting contributions.

## License

This project is licensed under the terms of the Apache License 2.0.
