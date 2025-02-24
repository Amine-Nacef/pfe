const mysql = require('mysql');
const fs = require('fs');
const express=require("express");
const app=express();
app.use(express.urlencoded({ extended: false }));
//app.use(express.json); le programme mamchach avec

var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    port: 3306,
    database: "pfe"
  });
  
  con.connect(function(err) {
    if (err) throw err;
    console.log('db ' + con.state);
  });

app.post("/ajouterutilisateur",(req,res)=>{
    const {nom,prenom,email,mot_de_passe,role}=req.body;

    con.query('SELECT * FROM utilisateurs WHERE email = ?', [email], (err, results) => {
        if (err) {
          return res.status(500).send("utilisateur n'a pas pu etre identifier avant d'étre ajouté");
        }
    
        if (results.length > 0) {

          return res.status(400).send('Utilisateur avec cette email existe deja');
        } else {
    var sql = "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES (?,?,?,?,?);";
  con.query(sql,[nom,prenom,email,mot_de_passe,role] , function (err, result) {
    if (err) {
        return res.status(500).send("utilisateur n'a pas pu etre ajouter");
      }
    console.log("utilisateur ajouter");
  });
}
    });
});

app.post("/ajouterfuite",(req,res)=>{
  fs.readFile('./scrap_result/donnees.json', 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading the file:', err);
    }else{

      const parsedData = JSON.parse(data);
    
      parsedData.forEach(item => {

    con.query('SELECT * FROM fuite WHERE information = ?', [item.titre], (err, results) => {
        if (err) {
          return res.status(500).send("la fuite n'a pas pu etre identifier avant d'étre ajouté");
        }
    
        if (results.length > 0) {

          return res.status(400).send('information existe deja');
        } else {
    var sql = "INSERT INTO fuite (information,lien,source,date) VALUES (?,?,?,?);";
  con.query(sql,[item.titre,item.lien,item.source,item.date] , function (err, result) {
    if (err) {
        return res.status(500).send("l'information n'a pas pu etre ajouter");
      }
    console.log("information ajouter");
  });
}
    });
});
}});
});

app.get("/extrairefuite",(req,res)=>{
  id=req.query.id;
  con.query("SELECT * FROM fuite WHERE id= ?;",[id], function (err, result) {
    if (err) {
        return res.status(500).send("la fuite n'a pas pu etre extrait");
      }
    res.json(result[0]);
  });
})
app.listen(3000,()=>{
  console.log("server is running on port 3000");
});
app.get("/extrairefuite_ids", (req, res) => {
  con.query("SELECT id FROM fuite", (err, results) => {
      if (err) {
          return res.status(500).send("Erreur lors de l'extraction des IDs");
      }
      const ids = results.map(row => row.id);
      res.json(ids);
  });
});
app.get("/extrairefuite", (req, res) => {
  const id = req.query.id;
  if (!id) return res.status(400).send("ID manquant");

  con.query("SELECT information, lien, source, date FROM fuite WHERE id = ?;", [id], (err, result) => {
      if (err) {
          return res.status(500).send("Erreur lors de l'extraction de la fuite");
      }
      if (result.length === 0) {
          return res.status(404).send("Aucune donnée trouvée pour cet ID");
      }
      res.json(result[0]);
  });
});
