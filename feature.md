### 사용자가 글 작성
Method: POST  
URL: /posts  
```python
pymongo: db.stock.insert_one({  
     id: db.stock.count({})+1,  
    title: title,  
    content: content,  
    read: 0,  
    reg_date: datetime.now(),  
    mod_date: datetime.now()  
}) 
return id  
```
request: body: {  
    title: [제목],  
    content: [내용]  
}  
requirement: content, title  
response: body: {  
    id: [ID],  
    title: [제목],  
    content: [내용],  
    read: [조회수],  
    reg_date: [작성일],  
    mod_date: [수정일=작성일]  
}  