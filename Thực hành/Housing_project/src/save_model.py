import os
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error


def save_best_model(best_model, best_name, best_rmse, scaler, 
                    X_validation, Y_validation, models_dir='../models', results_dir='../results'):
    """
    Lưu model, scaler, và báo cáo kết quả.
    
    Parameters:
    -----------
    best_model : estimator
        Mô hình đã huấn luyện
    best_name : str
        Tên mô hình (ví dụ: 'LR', 'GBM')
    best_rmse : float
        RMSE từ cross-validation
    scaler : StandardScaler
        Scaler đã fit trên X_train
    X_validation : array
        Dữ liệu validation
    Y_validation : array
        Target của validation
    models_dir : str
        Thư mục lưu model (mặc định: '../models')
    results_dir : str
        Thư mục lưu kết quả (mặc định: '../results')
    
    Returns:
    --------
    dict : {
        'model_path': str,
        'scaler_path': str,
        'validation_rmse': float
    }
    """
    
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    # Đánh giá trên validation set
    X_val_scaled = scaler.transform(X_validation)
    preds = best_model.predict(X_val_scaled)
    rmse_val = np.sqrt(mean_squared_error(Y_validation, preds))
    
    # Lưu model
    model_path = os.path.join(models_dir, 'best_model.joblib')
    joblib.dump(best_model, model_path)
    
    # Lưu scaler
    scaler_path = os.path.join(models_dir, 'scaler.joblib')
    joblib.dump(scaler, scaler_path)
    
    # Lưu báo cáo metadata
    metadata = {
        'model_name': best_name,
        'cv_rmse': best_rmse,
        'validation_rmse': rmse_val,
        'model_type': type(best_model).__name__
    }
    metadata_path = os.path.join(models_dir, 'metadata.txt')
    with open(metadata_path, 'w') as f:
        for key, val in metadata.items():
            f.write(f"{key}: {val}\n")
    
    print("=" * 60)
    print(" MODEL SAVED SUCCESSFULLY")
    print("=" * 60)
    print(f"Model: {best_name} ({type(best_model).__name__})")
    print(f"CV RMSE: {best_rmse:.4f}")
    print(f"Validation RMSE: {rmse_val:.4f}")
    print(f"\nPaths:")
    print(f"  - Model: {model_path}")
    print(f"  - Scaler: {scaler_path}")
    print(f"  - Metadata: {metadata_path}")
    print("=" * 60)
    
    return {
        'model_path': model_path,
        'scaler_path': scaler_path,
        'validation_rmse': rmse_val
    }


def load_best_model(models_dir='../models'):
    """
    Load model và scaler đã lưu.
    
    Parameters:
    -----------
    models_dir : str
        Thư mục chứa model (mặc định: '../models')
    
    Returns:
    --------
    dict : {
        'model': estimator,
        'scaler': StandardScaler,
        'model_path': str,
        'scaler_path': str
    }
    """
    
    model_path = os.path.join(models_dir, 'best_model.joblib')
    scaler_path = os.path.join(models_dir, 'scaler.joblib')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f" Không tìm thấy model tại: {model_path}\n"
            "Hãy chạy phần 'Tóm tắt kết quả' trong Evaluate Algorithms.ipynb trước!"
        )
    
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(
            f" Không tìm thấy scaler tại: {scaler_path}\n"
            "Hãy chạy phần 'Tóm tắt kết quả' trong Evaluate Algorithms.ipynb trước!"
        )
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    print("=" * 60)
    print(" MODEL LOADED SUCCESSFULLY")
    print("=" * 60)
    print(f"Model: {type(model).__name__}")
    print(f"Scaler: {type(scaler).__name__}")
    print(f"\nPaths:")
    print(f"  - Model: {model_path}")
    print(f"  - Scaler: {scaler_path}")
    print("=" * 60)
    
    return {
        'model': model,
        'scaler': scaler,
        'model_path': model_path,
        'scaler_path': scaler_path
    }


def evaluate_on_validation(model, scaler, X_validation, Y_validation):
    """
    Đánh giá model trên validation set.
    
    Parameters:
    -----------
    model : estimator
        Mô hình đã huấn luyện
    scaler : StandardScaler
        Scaler đã fit
    X_validation : array
        Dữ liệu validation
    Y_validation : array
        Target của validation
    
    Returns:
    --------
    dict : {
        'mse': float,
        'rmse': float,
        'predictions': array,
        'errors': array
    }
    """
    
    X_val_scaled = scaler.transform(X_validation)
    predictions = model.predict(X_val_scaled)
    
    mse = mean_squared_error(Y_validation, predictions)
    rmse = np.sqrt(mse)
    errors = Y_validation - predictions
    
    print("=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Mean Absolute Error (MAE): {np.mean(np.abs(errors)):.4f}")
    print("=" * 60)
    
    return {
        'mse': mse,
        'rmse': rmse,
        'predictions': predictions,
        'errors': errors
    }


def save_predictions(Y_actual, Y_predicted, output_path='../results/predictions.csv'):
    """
    Lưu kết quả dự đoán vào file CSV.
    
    Parameters:
    -----------
    Y_actual : array
        Giá trị thực tế
    Y_predicted : array
        Giá trị dự đoán
    output_path : str
        Đường dẫn file CSV output
    
    Returns:
    --------
    str : Đường dẫn file đã lưu
    """
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    errors = Y_actual - Y_predicted
    abs_errors = np.abs(errors)
    
    df = pd.DataFrame({
        'Y_actual': Y_actual,
        'Y_predicted': Y_predicted,
        'Error': errors,
        'Abs_Error': abs_errors
    })
    
    df.to_csv(output_path, index=False)
    
    print(f"✓ Predictions saved to: {output_path}")
    
    return output_path
