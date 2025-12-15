cd "C:/Users/ASUS/Documents/SGU_khai_pha_du_lieu_DDU1231"


Tạo thư mục demo/lab02 (nếu chưa có):
mkdir demo\lab02

Di chuyển file vào demo/lab02
move SGU_KPDL_Lab02_Pima_Indians_Diabetes.pptx demo\lab02\


git add demo/lab02/SGU_KPDL_Lab02_Pima_Indians_Diabetes.pptx
git commit -m "Add Lab02 PowerPoint (Pima Indians Diabetes) in demo/lab02"
git push origin main



# Mẫu chuẩn VS Code terminal
cd "C:\Users\ASUS\Documents\SGU_khai_pha_du_lieu_DDU1231"
git status --porcelain
git remote -v
git pull origin main --rebase
git add "demo/LabXX/<filename>"
git commit -m "Add LabXX: <description>"
git rev-parse --short HEAD
git push origin main
